import logging
from datetime import datetime
from os import path

import config


def get_file_handler(file_name: str, parent_dir: str):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
    handler = logging.FileHandler(path.join(
        parent_dir, config.LOG_FILE_HANDLER_NAME.format(file_name=file_name, timestamp=timestamp)
    ))
    handler.setLevel(config.LOG_FILE_HANDLER_LEVEL)
    handler.setFormatter(logging.Formatter(config.LOG_FILE_HANDLER_FORMAT))
    return handler


def get_stream_handler():
    handler = logging.StreamHandler()
    handler.setLevel(config.LOG_STREAM_HANDLER_LEVEL)
    handler.setFormatter(logging.Formatter(config.LOG_STREAM_HANDLER_FORMAT))
    return handler


def get_logger(logger_name: str, file_name: str, parent_dir: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        logger.addHandler(get_stream_handler())
        logger.addHandler(get_file_handler(file_name=file_name, parent_dir=parent_dir))
    return logger


def update_file_handler(logger: logging.Logger, file_name: str, parent_dir: str):
    file_handler = get_file_handler(file_name, parent_dir)
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
    logger.addHandler(file_handler)


def update_task_file_handler(logger: logging.Logger, file_name: str):
    return update_file_handler(logger=logger, file_name=file_name, parent_dir=config.LOG_TASK_PARENT_DIR)
