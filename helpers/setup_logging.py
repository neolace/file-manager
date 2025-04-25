import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: Optional[Path] = None,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        log_file: Path to the log file
        console_level: Logging level for console output
        file_level: Logging level for file output

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("file_manager")
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to prevent duplicate logs
    logger.handlers.clear()

    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_file = Path(log_file)
        if log_file.parent:
            log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")

    return logger
