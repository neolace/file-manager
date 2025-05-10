import shutil
from logging import Logger, getLogger
from pathlib import Path
from typing import Optional, List, Sequence

# Constants
HIDDEN_PREFIX = "."
DEFAULT_LOGGER_NAME = __name__

# Custom type hints
PathSequence = Sequence[Path]


def create_default_logger() -> Logger:
    """Create and return a default logger instance."""
    return getLogger(DEFAULT_LOGGER_NAME)


def find_hidden_folders(root_path: Path, excluded_names: List[str]) -> PathSequence:
    """
    Find all hidden folders in the given path, excluding specified names.

    Args:
        root_path: The root path to search for hidden folders
        excluded_names: List of folder names to exclude

    Returns:
        List of hidden folder paths, sorted by depth (deepest first)
    """
    hidden_folders = [
        item
        for item in root_path.rglob("*")
        if item.is_dir()
        and item.name.startswith(HIDDEN_PREFIX)
        and item.name not in excluded_names
    ]
    return sorted(hidden_folders, key=lambda x: len(x.parts), reverse=True)


def delete_folder(folder_path: Path, logger: Logger) -> None:
    """
    Delete a folder and log the result.

    Args:
        folder_path: Path to the folder to delete
        logger: Logger instance for output
    """
    try:
        shutil.rmtree(folder_path)
        logger.info(f"Deleted hidden folder: {folder_path}")
    except OSError as e:
        logger.error(f"Error deleting hidden folder {folder_path}: {e}")


def delete_all_hidden_folders(
    path: Path,
    excluded_names: Optional[List[str]] = None,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Delete all hidden folders (starting with '.') within the specified path.

    Args:
        path: The path to search for hidden folders
        excluded_names: List of hidden folder names to exclude from deletion
        dry_run: If True, only log actions without deleting anything
        logger: Logger instance for output
    """
    active_logger = logger or create_default_logger()

    if not path.exists() or not path.is_dir():
        active_logger.warning(f"Directory does not exist or is not a directory: {path}")
        return

    hidden_folders = find_hidden_folders(path, excluded_names or [])

    for folder in hidden_folders:
        if dry_run:
            active_logger.info(f"Would delete hidden folder: {folder}")
        else:
            delete_folder(folder, active_logger)