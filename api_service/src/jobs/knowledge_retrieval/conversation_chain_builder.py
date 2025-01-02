from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import USE_CHAT_HISTORY_IN_CONTEXT
from core.loggers import server_logger as logger
from init_models import LLM_MODEL


class ConversationChainBuilder:

    def __init__(self, retriever):
        self.retriever = retriever

    @staticmethod
    def get_prompt():
        template = """
            <|system|>>
            You are an AI assistant that follows instructions extremely well.
            Please be truthful and give direct answers.
            Please tell "I don't know" if the user query is not in the context and ask for more 
            information in short words.
        
            CONTEXT: {context}
            </s>
            <|user|>
            {query_text}
            </s>
            <|assistant|>
            """

        prompt = ChatPromptTemplate.from_template(template)
        return prompt

    @staticmethod
    def get_session_history(session_id) -> RedisChatMessageHistory:
        chat_history = RedisChatMessageHistory(session_id, url="redis://redis:6379/0")
        # todo: change this to overwrite the oldest message after 5 messages
        if len(chat_history.messages) >= 10:
            chat_history.clear()
        return chat_history

    def get_chain_with_chat_history_context(self):
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            LLM_MODEL, self.retriever, contextualize_q_prompt
        )

        qa_system_prompt = """You are an AI assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        Please be truthful and give direct answers. \
        If you don't know the answer, just say that you don't know and ask for \
        more information in short words.\
        
        {context}"""
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(LLM_MODEL, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        chain = rag_chain | RunnableLambda(self.inspect)

        conversational_rag_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        return conversational_rag_chain

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def inspect(state):
        logger.debug(f"State: {state}")
        return state

    def get_chain_without_chat_history_context(self):
        chain_from_docs = (
                RunnablePassthrough.assign(context=(lambda x: self.format_docs(x["context"])))
                | RunnableLambda(self.inspect)
                | self.get_prompt()
                | LLM_MODEL
                | StrOutputParser()
        )

        chain = RunnableParallel(
            {"context": self.retriever, "query_text": RunnablePassthrough()}
        ).assign(answer=chain_from_docs)

        return chain

    def build_chain(self):
        chain = None
        if USE_CHAT_HISTORY_IN_CONTEXT:
            chain = self.get_chain_with_chat_history_context()
        else:
            chain = self.get_chain_without_chat_history_context()

        return chain
