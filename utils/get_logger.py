from logging import Logger
from pathlib import Path
from typing import Optional

from utils.setup_logging import setup_logging

# Default log file path if none is provided
DEFAULT_LOG_PATH = Path('logs/app.log')

def configure_logger(log_file: Optional[Path] = DEFAULT_LOG_PATH) -> Logger:
    """
    Configure and return a centralized logger instance.

    Args:
        log_file (Optional[Path]): Path to the log file. If not provided,
                                 DEFAULT_LOG_PATH will be used.

    Returns:
        Logger: Configured logging instance ready for use.
    """
    return setup_logging(log_file=log_file)