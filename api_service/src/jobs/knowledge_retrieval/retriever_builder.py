from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_community.retrievers import BM25Retriever

from init_models import RERANKER_MODEL
from jobs.process_dataset.chroma_repository import get_chroma_client
from jobs.process_dataset.document_chunker import load_chunks


class RetrieverBuilder:

    def __init__(self, topic):
        self.topic = topic

    def build_vectorstore_retriever(self):
        vectorstore = get_chroma_client(collection=self.topic)
        return vectorstore.as_retriever()

    def build_keyword_retriever(self):
        chunked_docs = load_chunks(topic_slug=self.topic)
        if chunked_docs is not None:
            keyword_retriever = BM25Retriever.from_documents(chunked_docs)
            keyword_retriever.k = 5
            return keyword_retriever
        else:
            raise Exception("No chunks available for the topic")

    def build_search_retriever(self):
        vectorstore_retriever = self.build_vectorstore_retriever()
        keyword_retriever = self.build_keyword_retriever()
        ensemble_retriever = EnsembleRetriever(retrievers=[vectorstore_retriever, keyword_retriever],
                                               weights=[0.5, 0.5])
        return ensemble_retriever

    @staticmethod
    def build_reranker():
        return RERANKER_MODEL

    def build_retriever(self):
        search_retriever = self.build_search_retriever()
        reranker = self.build_reranker()
        retriever = ContextualCompressionRetriever(
            base_compressor=reranker, base_retriever=search_retriever
        )
        return retriever
