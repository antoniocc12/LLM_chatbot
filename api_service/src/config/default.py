# APP Configs
APP_MEDIA_ROOT = "/uploads"

# Database Configs
DATABASE_ENGINE = "django.db.backends.postgresql"
DATABASE_NAME = "chatbot"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "admin"
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432

# Celery Configs
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

# Log Configs
LOG_STREAM_HANDLER_LEVEL = "DEBUG"
LOG_STREAM_HANDLER_FORMAT = "[%(asctime)s | %(levelname)s | %(funcName)s()] %(message)s"
LOG_FILE_HANDLER_NAME = "{timestamp}_{file_name}.log"
LOG_FILE_HANDLER_LEVEL = "DEBUG"
LOG_FILE_HANDLER_FORMAT = "[%(asctime)s | %(levelname)s | %(funcName)s()] %(message)s"
LOG_TASK_PARENT_DIR = "/logs/tasks"
LOG_SERVER_PARENT_DIR = "/logs/server"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "BAAI/bge-reranker-base"
LLM_MODEL_NAME = "stablelm-zephyr"

OLLAMA_URL = "http://ollama:11434"

USE_CHAT_HISTORY_IN_CONTEXT = False
HIDE_PII = True
PII_ENTITIES = "PHONE,EMAIL"
REPLACE_PII_WITH_FAKE_DATA = False

MODELS_PATH = "../data/models/"
CHROMA_PATH = "../data/chromadb/"
