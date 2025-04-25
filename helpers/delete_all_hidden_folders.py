import shutil
from logging import Logger
from pathlib import Path
from typing import Optional, List


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
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    if not path.exists() or not path.is_dir():
        logger.warning(f"Directory does not exist or is not a directory: {path}")
        return

    excluded_names = excluded_names or []

    hidden_folders = [
        item
        for item in path.rglob("*")
        if item.is_dir()
        and item.name.startswith(".")
        and item.name not in excluded_names
    ]
    hidden_folders.sort(key=lambda x: len(x.parts), reverse=True)

    for folder in hidden_folders:
        if dry_run:
            logger.info(f"Would delete hidden folder: {folder}")
        else:
            try:
                shutil.rmtree(folder)
                logger.info(f"Deleted hidden folder: {folder}")
            except OSError as e:
                logger.error(f"Error deleting hidden folder {folder}: {e}")
