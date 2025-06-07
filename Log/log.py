import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

class WatchmanLogger:
    def __init__(self, log_file: str = "logs/Watchman.log", log_level=logging.DEBUG, max_bytes: int = 1024, backup_count: int = 5):
        self.log_file = log_file
        self.log_level = log_level
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.logger = logging.getLogger("watchman_logger")
        self.logger.setLevel(self.log_level)
        self._setup_handlers()

    def _setup_handlers(self):
        if self.logger.handlers:
            return

        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8',
            mode='a'
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        ))

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def info(self, msg: str): 
        self.logger.info(msg)

    def debug(self, msg: str): 
        self.logger.debug(msg)

    def warning(self, msg: str): 
        self.logger.warning(msg)

    def error(self, msg: str): 
        self.logger.error(msg)

    def critical(self, msg: str): 
        self.logger.critical(msg)

    def exception(self, msg: str, exc: Optional[Exception] = None):
        self.logger.error(f"{msg} - Exception: {exc}", exc_info=True)
