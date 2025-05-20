import os
from logging import Logger, getLogger
from pathlib import Path
from typing import Optional


def remove_folder_by_name(
        root: Path, target_name: str, dry_run: bool = False, logger: Optional[Logger] = None
) -> None:
    """
    Remove all folders with a specific name within a given root path.

    Args:
        root: The root directory to search in
        target_name: Name of the folders to remove
        dry_run: If True, only log actions without performing them
        logger: Optional logger instance, defaults to root logger if None
    """
    logger = logger or getLogger()

    if not _validate_root_path(root, logger):
        return

    folders = list(root.rglob("*"))
    for folder in folders:
        if folder.is_dir() and folder.name == target_name:
            _delete_folder(folder, dry_run, logger)


def _validate_root_path(path: Path, logger: Logger) -> bool:
    """Validate that the root path exists."""
    if not path.exists():
        logger.error(f"Root path does not exist: {path}")
        return False
    return True


def _delete_folder(folder: Path, dry_run: bool, logger: Logger) -> None:
    """Delete a folder or log the action in dry run mode."""
    if dry_run:
        logger.info(f"Would delete: {folder}")
    else:
        try:
            os.rmdir(folder)
            logger.info(f"Deleted contents of: {folder}")
        except OSError as e:
            logger.error(f"Error deleting {folder}: {e}")
