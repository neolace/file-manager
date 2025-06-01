from logging import Logger
from pathlib import Path
from typing import Optional

from config.settings import Config
from utils.setup_logging import setup_logging


def configure_logger(log_file: Optional[Path] = Config.DEFAULT_LOG_PATH) -> Logger:
    """
    Configure and return a centralized logger instance.

    Args:
        log_file (Optional[Path]): Path to the log file. If not provided,
                                 DEFAULT_LOG_PATH will be used.

    Returns:
        Logger: Configured logging instance ready for use.
    """
    return setup_logging(log_file=log_file,
                         log_level_str=Config.DEFAULT_LOG_LEVEL)
