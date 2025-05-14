import shutil
from logging import Logger
from pathlib import Path
from typing import List, Optional, Union

# Type aliases for better clarity
PathItem = Union[Path, str]
ExcludedItems = List[str]

# Constants for log messages
LOG_MESSAGES = {
    "INVALID_DIR": "Directory does not exist or is not a directory: {}",
    "SKIP_EXCLUDED": "Skipping excluded item: {}",
    "WOULD_DELETE": "Would delete: {}",
    "DELETED_FILE": "Deleted file: {}",
    "DELETED_DIR": "Deleted directory: {}",
    "DELETE_ERROR": "Error deleting {}: {}",
}


def delete_all_files_folders_within_folder(
    directory_path: Path,
    excluded_names: Optional[ExcludedItems] = None,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Delete all files and folders within the specified folder.

    Args:
        directory_path: The path to the folder to clean
        excluded_names: List of file/folder names to exclude from deletion
        dry_run: If True, only log actions without deleting anything
        logger: Logger instance for output
    """
    logger = logger or _get_default_logger()

    if not _is_valid_directory(directory_path):
        logger.warning(LOG_MESSAGES["INVALID_DIR"].format(directory_path))
        return

    excluded_names = excluded_names or []

    for item in directory_path.iterdir():
        _process_item(item, excluded_names, dry_run, logger)


def _get_default_logger() -> Logger:
    """Create and return a default logger."""
    import logging

    return logging.getLogger(__name__)


def _is_valid_directory(path: Path) -> bool:
    """Check if the given path is a valid directory."""
    return path.exists() and path.is_dir()


def _process_item(
    item: Path, excluded_names: ExcludedItems, dry_run: bool, logger: Logger
) -> None:
    """Process a single file system item for deletion."""
    if item.name in excluded_names:
        logger.info(LOG_MESSAGES["SKIP_EXCLUDED"].format(item))
        return

    if dry_run:
        logger.info(LOG_MESSAGES["WOULD_DELETE"].format(item))
        return

    try:
        _delete_item(item, logger)
    except Exception as e:
        logger.error(LOG_MESSAGES["DELETE_ERROR"].format(item, e))


def _delete_item(item: Path, logger: Logger) -> None:
    """Delete a file system item and log the action."""
    if item.is_file() or item.is_symlink():
        item.unlink()
        logger.info(LOG_MESSAGES["DELETED_FILE"].format(item))
    elif item.is_dir():
        shutil.rmtree(item)
        logger.info(LOG_MESSAGES["DELETED_DIR"].format(item))
