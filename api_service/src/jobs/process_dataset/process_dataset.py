import traceback

from celery import Celery

from chatbot.models import Dataset, ProcessingStatus
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from core.exceptions import TaskFailure
from core.loggers import task_logger as logger
from jobs.process_dataset.chroma_repository import persist_embeddings
from jobs.process_dataset.document_chunker import chunk_document, persist_chunks
from jobs.process_dataset.document_loader import load_documents
from jobs.process_dataset.utils.task import register_task, task_completed, update_task_current_status

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(track_started=True)
def process_dataset_task(dataset_id):
    task_id = process_dataset_task.request.id
    task = register_task(task_id=task_id)

    result = {"status": "success"}
    try:
        logger.info(f"Starting the data processing...")
        logger.info(f"Task ID: {task_id}")
        dataset = Dataset.objects.get(id=dataset_id)
        logger.info(f"Processing dataset {dataset}")
        task = update_task_current_status(task, ProcessingStatus.LOADING)
        document = load_documents(dataset.file.path)
        logger.info(f"Loaded document")
        task = update_task_current_status(task, ProcessingStatus.LOADED)
        task = update_task_current_status(task, ProcessingStatus.CHUNKING)
        chunks = chunk_document(document)
        logger.info(f"Chunked document")
        task = update_task_current_status(task, ProcessingStatus.CHUNKED)
        task = update_task_current_status(task, ProcessingStatus.STORING)
        persist_embeddings(topic_slug=dataset.topic.slug,
                           chunks=chunks, filename=dataset.name)
        logger.info("Stored documents")
        task = update_task_current_status(task, ProcessingStatus.STORED)

    except Exception as e:
        err_msg = f"Data Processing Failed. ERROR_DESC: {e}"
        logger.exception(err_msg, exc_info=e)
        raise TaskFailure(detail=err_msg, task=task, tb=traceback.format_exc())

    logger.info(f"Data Processing Completed Successfully.")
    return task_completed(task=task, result=result)
