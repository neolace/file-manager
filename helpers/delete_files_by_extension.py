from logging import Logger
from pathlib import Path
from typing import List, Optional


def delete_files_by_extension(
    path: Path,
    extensions: List[str],
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Delete all files with the specified extensions in the given path.

    Args:
        path: The directory path to search for files
        extensions: List of file extensions to delete (without dots)
        dry_run: If True, only log actions without deleting files
        logger: Logger instance for output
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    normalized_extensions = [ext.lower().lstrip(".") for ext in extensions]

    try:
        for item in path.rglob("*"):
            if (
                item.is_file()
                and item.suffix.lower().lstrip(".") in normalized_extensions
            ):
                if dry_run:
                    logger.info(f"Would delete file: {item}")
                else:
                    try:
                        item.unlink()
                        logger.info(f"Deleted file: {item}")
                    except OSError as e:
                        logger.error(f"Error deleting file {item}: {e}")
    except OSError as e:
        logger.error(f"Error accessing {path}: {e}")
