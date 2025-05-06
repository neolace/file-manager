from logging import Logger
from pathlib import Path
from typing import Optional


def get_logger(log_file: Optional[Path] = None) -> Logger:
    """
    Get a centralized logger instance.

    Args:
        log_file: Optional log file path.
    """
    from utils.setup_logging import setup_logging
    return setup_logging(log_file=log_file)