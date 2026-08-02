# utils/setup_logging.py
import logging
from pathlib import Path


def setup_logging(log_file: Path, log_level_str: str) -> logging.Logger:
    """
    Sets up the logging configuration with error handling.

    :param log_file: Path to the log file.
    :param log_level_str: Logging level as a string (e.g., "INFO", "DEBUG").
    :return: Configured logger instance.
    """
    numeric_level = getattr(logging, log_level_str.upper(), logging.INFO)

    logger = logging.getLogger("file_manager")
    logger.setLevel(numeric_level)

    try:
        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)

        # Define log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
            "[%(filename)s:%(lineno)d]"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    except (OSError, IOError) as e:
        # Handle logging setup failure
        logger.error(f"Failed to set up file logging: {e}")
        logger.warning("Falling back to console-only logging.")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console_handler)

    return logger
