import shutil
from logging import Logger
from pathlib import Path
from typing import List, Optional


def delete_dot_folders_recursive(
    path: Path,
    excluded_names: Optional[List[str]] = None,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Recursively find and delete folders that start with a dot (hidden folders).

    Args:
        path: The path to start searching for dot folders
        excluded_names: List of folder names to exclude from deletion
        dry_run: If True, only log actions without deleting anything
        logger: Logger instance for output
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    excluded_names = excluded_names or []

    try:
        dot_folders = [
            item
            for item in path.rglob("*")
            if item.is_dir()
            and item.name.startswith(".")
            and item.name not in excluded_names
        ]
        dot_folders.sort(key=lambda x: len(x.parts), reverse=True)

        for folder in dot_folders:
            if dry_run:
                logger.info(f"Would delete dot folder: {folder}")
            else:
                try:
                    shutil.rmtree(folder)
                    logger.info(f"Deleted dot folder: {folder}")
                except OSError as e:
                    logger.error(f"Error deleting dot folder {folder}: {e}")
    except OSError as e:
        logger.error(f"Error accessing {path}: {e}")
