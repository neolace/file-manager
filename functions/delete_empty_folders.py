from logging import Logger
from pathlib import Path
from typing import Optional


def delete_empty_folders(
    path: Path, dry_run: bool = False, logger: Optional[Logger] = None
) -> None:
    """
    Recursively loop through all folders and subfolders in the given path,
    deleting only empty folders.

    Args:
        path: Path to start deletion from
        dry_run: If True, only show what would be deleted without actually deleting
        logger: Logger instance for output
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    try:
        # Iterate through all items in the current path
        for item in path.iterdir():
            # Check if the item is a directory
            if item.is_dir():
                # Recursively process subfolders first
                delete_empty_folders(item, dry_run, logger)
                # After processing subfolders, check if the current folder is empty
                try:
                    if not dry_run:
                        item.rmdir()  # rmdir only deletes empty directories
                        logger.info(f"Deleted empty folder: {item}")
                    else:
                        # Check if directory is empty to simulate deletion
                        if not any(item.iterdir()):
                            logger.info(f"Would delete empty folder: {item}")
                except OSError:
                    # Folder is not empty or cannot be deleted
                    pass
    except OSError as e:
        logger.error(f"Error accessing {path}: {e}")
