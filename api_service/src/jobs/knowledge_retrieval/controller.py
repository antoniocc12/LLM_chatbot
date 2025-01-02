from chatbot.models import History, Topic
from config import USE_CHAT_HISTORY_IN_CONTEXT
from core.loggers import server_logger as logger
from jobs.knowledge_retrieval.conversation_chain_builder import ConversationChainBuilder
from jobs.knowledge_retrieval.retriever_builder import RetrieverBuilder


def start_knowledge_retrieval(query: str, topic: str, user: str) -> dict:
    """
    This method will execute the steps to retrieve the answer for the query
    :return: dict with answer and its related information
    """
    try:
        logger.info(f"Starting the knowledge retrieval...")

        retriever_builder_obj = RetrieverBuilder(topic=topic)
        # build the retriever with hybrid search and reranking capabilities
        retriever = retriever_builder_obj.build_retriever()
        logger.debug("Build retriever - completed")

        conversation_chain_builder_obj = ConversationChainBuilder(retriever=retriever)
        # build the conversation chain with retriever, llm, prompt and chat history
        chain = conversation_chain_builder_obj.build_chain()
        logger.debug("Build conversation chain - completed")

        if USE_CHAT_HISTORY_IN_CONTEXT:
            result = chain.invoke(
                {"input": query},
                config={"configurable": {"session_id": f"{user}__{topic}"}}
            )
        else:
            result = chain.invoke(query)

        logger.info(f"The result: \n {result}")
        answer = result["answer"]
        document_metadata = result["context"][0].metadata
        metadata = {
            "source": document_metadata.get("id").split(":")[0].strip(),
            "page_no": int(document_metadata.get("page", 0)) + 1
        }
        context = [doc.page_content for doc in result["context"]]

        # store the messages in database table
        History.objects.create(query=query, answer=answer, metadata=metadata,
                               user_created=user, topic=Topic.objects.get(slug=topic))

        logger.info(f"Knowledge Retrieval is completed successfully.")

        return {
            "answer": answer,
            "metadata": metadata,
            "context": context
        }

    except Exception as e:
        err_msg = f"Knowledge retrieval Failed. ERROR_DESC: {e}"
        logger.exception(err_msg, exc_info=e)
        raise Exception(str(e))


