import shutil
from logging import Logger
from pathlib import Path
from typing import List, Optional


def delete_all_files_folders_within_folder(
    path: Path,
    excluded_names: Optional[List[str]] = None,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Delete all files and folders within the specified folder.

    Args:
        path: The path to the folder
        excluded_names: List of file/folder names to exclude from deletion
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

    for item in path.iterdir():
        if item.name in excluded_names:
            logger.info(f"Skipping excluded item: {item}")
            continue
        if dry_run:
            logger.info(f"Would delete: {item}")
        else:
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                    logger.info(f"Deleted file: {item}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    logger.info(f"Deleted directory: {item}")
            except Exception as e:
                logger.error(f"Error deleting {item}: {e}")
