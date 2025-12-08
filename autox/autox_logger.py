# Define and use customized logger
# For this create three objects:
# logger
# handler:
# StreamHandler: prints to console
# FileHandler: prints to file
# SMTPHandler: sends logs over email
# HTTPHandler: sends logs to a app server using http protocol
# formatter: Responsible for formatting log message
# After creating these objects, we need to associate formatter object to handler object.
# Then associate handler object to logger object

import logging
import os
from datetime import datetime
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
LOG_FOLDER_NAME = "autox_logs"
LOG_FILE_NAME = "autox_logs.log"
# DATE_TIME_FORMAT = "%b-%d %H:%M:%S"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SET_LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "DEBUG").upper())


def set_autox_log_path():
    # Use a filesystem-safe timestamp (avoid ':' which is invalid on Windows)
    time_format = "run-%Y-%m-%d-%H-%M-%S"
    timestamp_directory = datetime.now().strftime(time_format)
    log_dir = REPOSITORY_ROOT / LOG_FOLDER_NAME / timestamp_directory
    # Create directories recursively and tolerate existing dirs
    log_dir.mkdir(parents=True, exist_ok=True)

    return log_dir


class ColorFormatter(logging.Formatter):
    """Custom logging formatter with ANSI colors."""

    COLORS = {
        "TRACE": "\033[96m",
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        record.levelname_colored = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger():
    log_path = set_autox_log_path() / LOG_FILE_NAME

    # Create logger object and set-level
    logger = logging.getLogger(__name__)
    logger.setLevel(SET_LOG_LEVEL)

    logger.propagate = False

    # Create formatter object
    color_formatter = ColorFormatter(
        "%(asctime)s - %(name)s - %(levelname_colored)s >>> %(message)s > %(filename)s:line:%(lineno)d",
        datefmt=DATE_TIME_FORMAT,
    )
    plain_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s >>> %(message)s > %(filename)s:line:%(lineno)d",
        datefmt=DATE_TIME_FORMAT,
    )

    if not logger.handlers:
        # Create handler object and set-level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(SET_LOG_LEVEL)
        # Associate formatter and handler object
        console_handler.setFormatter(color_formatter)
        # Associate handler and logger object
        logger.addHandler(console_handler)

        # Create handler object and set-level
        file_handler = logging.FileHandler(str(log_path), mode="w")
        file_handler.setLevel(SET_LOG_LEVEL)
        # Associate formatter and handler object
        file_handler.setFormatter(plain_formatter)
        # Associate handler and logger object
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()
