import os

from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.ollama import Ollama

from config import MODELS_PATH, OLLAMA_URL, EMBEDDING_MODEL_NAME, RERANKER_MODEL_NAME, LLM_MODEL_NAME
from jobs.utils.general import dump_to_pickle, load_from_pickle

EMBEDDING_MODEL = None
RERANKER_MODEL = None
LLM_MODEL = None


def load_models():
    os.makedirs(MODELS_PATH, exist_ok=True)

    embedding_model_path = os.path.join(MODELS_PATH, "embedding_model.pkl")
    reranker_model_path = os.path.join(MODELS_PATH, "reranker_model.pkl")
    models_list = []
    if not os.path.exists(embedding_model_path):
        print("Downloading embedding model..")
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        models_list.append({"data": embedding_model, "path": embedding_model_path})
        print("Downloaded embedding model")
    if not os.path.exists(reranker_model_path):
        print("Downloading reranking model..")
        model = HuggingFaceCrossEncoder(model_name=RERANKER_MODEL_NAME)
        reranker_model = CrossEncoderReranker(model=model, top_n=1)
        models_list.append({"data": reranker_model, "path": reranker_model_path})
        print("Downloaded reranking model")

    for item in models_list:
        dump_to_pickle(**item)

    load_embedding_model(embedding_model_path)
    load_reranker_model(reranker_model_path)
    load_llm_model()


def load_embedding_model(path):
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is None:
        EMBEDDING_MODEL = load_from_pickle(path)


def load_reranker_model(path):
    global RERANKER_MODEL
    if RERANKER_MODEL is None:
        RERANKER_MODEL = load_from_pickle(path)


def load_llm_model():
    global LLM_MODEL
    if LLM_MODEL is None:
        LLM_MODEL = Ollama(base_url=OLLAMA_URL, model=LLM_MODEL_NAME, keep_alive=-1)
        LLM_MODEL.invoke("")
