import requests
import pandas as pd
from datasets import Dataset
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from ragas import evaluate
import os
from dotenv import load_dotenv
import logging
import sys

load_dotenv()

APP_HOST = os.getenv("APP_SERVER_HOST")
APP_PORT = os.getenv("APP_SERVER_PORT")
APP_OLLAMA_HOST = os.getenv("APP_OLLAMA_HOST")
APP_OLLAMA_PORT = os.getenv("APP_OLLAMA_PORT")
TOPIC = os.getenv("TOPIC")
DATASET_PATH = "data/test_dataset.csv"
RAGAS_MODEL_FOR_EVAL = os.getenv("RAGAS_MODEL_FOR_EVAL")
RESULT_PATH = "data/result.csv"

APP_CHATBOT_URL = "http://" + APP_HOST + ":" + APP_PORT + "/api/v1/chatbot"
APP_TOKEN_URL = APP_CHATBOT_URL + "/token"
APP_QUERY_URL = APP_CHATBOT_URL + "/topics" + "/" + TOPIC + "/query"

OLLAMA_URL = "http://" + APP_OLLAMA_HOST + ":" + APP_OLLAMA_PORT


def configure_and_get_logger():
    # Create and configure logger
    logging.basicConfig(filename="log.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


logger = configure_and_get_logger()


def get_embedding():
    return OllamaEmbeddings(model=RAGAS_MODEL_FOR_EVAL, base_url=OLLAMA_URL)


def get_llm():
    return Ollama(model=RAGAS_MODEL_FOR_EVAL, base_url=OLLAMA_URL)


def pull_ollama_model(model):
    logger.info(f"Pulling the model {model} in the Ollama server")
    response = requests.post(url=OLLAMA_URL + "/api/pull", json={"name": model, "stream": False})
    logger.info(response.content)


def get_access_token():
    grant_type = "password"
    username = "admin"
    password = "admin"
    client_id = "zMSG4Ieu8E0FZyctUh4uMjNrj41MpAkhzHDIheEK"
    body = {
        "grant_type": grant_type,
        "username": username,
        "password": password,
        "client_id": client_id
    }
    token_response = requests.post(APP_TOKEN_URL, data=body)
    logger.info(token_response.content)
    return token_response.json()["access_token"]


auth_token = get_access_token()
logger.info(f"Access Token - {auth_token}")
headers = {'Authorization': f'Bearer {auth_token}'}
url = APP_QUERY_URL
df = pd.read_csv(DATASET_PATH)
questions = []
contexts = []
ground_truths = []
answers = []
for index, row in df.iterrows():
    logger.info(row["query"])
    body = {
        "query": row["query"]
    }
    ground_truth = row["ground_truth"]
    logging.info(f"Sending Request to f{url} with body {body}")
    response = requests.post(url, json=body, headers=headers)
    response_body = response.json()
    logging.info(response_body)
    context = response_body["context"]
    answer = response_body["answer"]
    questions.append(row["query"])
    contexts.append(context)
    answers.append(answer)
    ground_truths.append(ground_truth)

ds = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
})

logger.info("Pull Ollama model before starting evaluation")
pull_ollama_model(model=RAGAS_MODEL_FOR_EVAL)
result = evaluate(ds, embeddings=get_embedding(), llm=get_llm())
df = result.to_pandas()
df.to_csv(path_or_buf=RESULT_PATH)
logger.info("Result is stored in data/result.csv")
