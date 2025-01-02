import logging

from chatbot.models import Task, ProcessingStatus
from core.loggers import task_logger as logger
from core.utils.logger import update_task_file_handler


def register_task(task_id):
    update_task_file_handler(logger=logger, file_name=task_id)
    task = Task.objects.get(task_id=task_id)
    task.status = Task.STARTED
    task.current_state = ProcessingStatus.STARTED.name
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            task.log = handler.baseFilename
    task.save()
    return task


def update_task_current_status(task, current_state):
    task.current_state = current_state.name
    task.save()
    return task


def task_completed(task, result):
    task.status = Task.SUCCESS
    task.current_state = ProcessingStatus.COMPLETED.name
    task.result = result
    task.save()
    return result
