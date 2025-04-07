import logging
import os


def setup_logging(level=logging.INFO, log_file=None):
    """
    Configure logging with appropriate format.

    Args:
        level: Logging level (default: INFO)
        log_file: Optional path to log file

    Returns:
        Root logger instance
    """
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    handlers.append(console_handler)

    # File handler if log_file is specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        handlers.append(file_handler)

    # Configure logging
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers if log_file else None
    )

    return logging.getLogger()  # Return root logger
