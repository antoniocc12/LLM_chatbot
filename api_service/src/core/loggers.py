from os import path

import config
from core.utils.logger import get_logger

task_logger = get_logger(logger_name="task", file_name="task", parent_dir=config.LOG_TASK_PARENT_DIR)
server_logger = get_logger(logger_name="server", file_name="server", parent_dir=config.LOG_SERVER_PARENT_DIR)
