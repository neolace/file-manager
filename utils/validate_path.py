from logging import Logger, getLogger
from pathlib import Path

from config.Config import Config


def get_default_logger() -> Logger:
    """Create and return a default logger instance."""
    return getLogger(__name__)


def validate_path(
    path: Path, require_existence: bool = True, logger: Logger | None = None
) -> bool:
    """
    Validate a file or directory path.

    Args:
        path: Path to validate.
        require_existence: Whether the path must exist.
        logger: Logger instance for output.

    Returns:
        bool: True if path validation passes, False otherwise.
    """
    current_logger = logger or get_default_logger()

    if require_existence and not path.exists():
        current_logger.error(Config.PATH_NOT_EXIST_ERROR.format(path))
        return False

    return True
