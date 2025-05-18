import logging
from pathlib import Path
from typing import Optional

from config.Config import Config
from utils.setup_logging import setup_logging

_logger: Optional[logging.Logger] = None


def _validate_log_level(log_level: str) -> str:
    """
    Validates the provided log level.

    Args:
        log_level: Log level to validate
    Returns:
        str: Uppercase log level string
    Raises:
        ValueError: If log level is invalid
    """
    try:
        level = log_level.upper()
        if not hasattr(logging, level):
            raise ValueError(f"Invalid log level: {log_level}")
        return level
    except AttributeError:
        raise ValueError(f"Invalid log level: {log_level}")


def get_logger(log_level: str = Config.DEFAULT_LOG_LEVEL) -> logging.Logger:
    """
    Returns a configured logger instance. Creates new logger if none exists.

    Args:
        log_level: Desired logging level (default: INFO)
    Returns:
        logging.Logger: Configured logger instance
    Raises:
        ValueError: If provided log_level is invalid
    """
    global _logger

    logging_level = _validate_log_level(log_level)

    if _logger is None:
        log_file = Path(Config.DEFAULT_LOG_FILENAME)
        _logger = setup_logging(log_file)
        _logger.setLevel(logging_level)

    return _logger
