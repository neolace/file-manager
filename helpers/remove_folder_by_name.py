import logging
from pathlib import Path

from helpers.delete_all_files_folders_within_folder import delete_all_files_folders_within_folder


def remove_folder_by_name(root_path: Path, folder_name: str, dry_run: bool = False, logger=None) -> None:
    """
    Find and remove all folders with the specified name.

    Args:
        root_path: The root directory to search in
        folder_name: Name of folders to remove
        dry_run: If True, only show what would be deleted without actually deleting
        logger: Logger instance for output
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    root = Path(root_path)
    count = 0

    for folder in root.rglob(folder_name):
        count += 1
        if dry_run:
            logger.info(f"Would delete: {folder}")
        else:
            try:
                delete_all_files_folders_within_folder(folder)
                logger.info(f"Deleted contents of: {folder}")
            except OSError as e:
                logger.error(f"Error deleting {folder}: {e}")

    logger.info(f"Processed {count} '{folder_name}' folders")
