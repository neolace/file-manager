# utils/setup_logging.py
import logging
from pathlib import Path


def setup_logging(log_file: Path) -> logging.Logger:
    """
    Sets up the logging configuration with error handling.

    :param log_file: Path to the log file.
    :return: Configured logger instance.
    """
    logger = logging.getLogger("file_manager")
    logger.setLevel(logging.DEBUG)  # Set default logging level to DEBUG

    try:
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Define log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
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
