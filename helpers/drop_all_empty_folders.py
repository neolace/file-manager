from logging import Logger
from pathlib import Path
from typing import Optional


def drop_all_empty_folders(
    path: Path,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Recursively find and delete all empty folders within the given path.
    Continues iterating until no more empty folders can be found.

    Args:
        path: The directory path to start cleaning
        dry_run: If True, only log actions without deleting folders
        logger: Logger instance for output
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    if not path.exists() or not path.is_dir():
        logger.warning(f"Path does not exist or is not a directory: {path}")
        return

    folders_deleted = True
    while folders_deleted:
        folders_deleted = False
        dirs = [d for d in path.rglob("*") if d.is_dir()]
        dirs.sort(key=lambda x: len(x.parts), reverse=True)

        for folder in dirs:
            try:
                if not any(folder.iterdir()):
                    if dry_run:
                        logger.info(f"Would delete empty folder: {folder}")
                    else:
                        folder.rmdir()
                        logger.info(f"Deleted empty folder: {folder}")
                        folders_deleted = True
            except Exception as e:
                logger.error(f"Error processing folder {folder}: {e}")
