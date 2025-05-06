from pathlib import Path


def validate_path(path: Path, must_exist: bool = True, logger=None) -> bool:
    """
    Validate a file or directory path.

    Args:
        path: Path to validate.
        must_exist: Whether the path must exist.
        logger: Logger instance for output.
    """
    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    if must_exist and not path.exists():
        logger.error(f"Path does not exist: {path}")
        return False
    return True