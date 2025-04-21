from logging import Logger
from pathlib import Path

from helpers.delete_all_files_folders_within_folder import (
    delete_all_files_folders_within_folder,
)


def remove_folder_by_name(root_path: Path, dry_run: bool = False, logger=None) -> None:
    """
    Find and remove all folders with the specified name.

    Args:
        root_path: The root directory to search in
        folder_name: Name of folders to remove
        dry_run: If True, only show what would be deleted without actually deleting
        logger: Logger instance for output
        :param folders:
    """
    if logger is None:
        logger: Logger = logger.setup_logging(log_file=Path("C:/tmp/file_manager.log"))

    root = Path(root_path)
    count = 0

    if not root.exists():
        logger.error(f"Root path does not exist: {root}")
        return

    for fldr in root.iterdir():
        folder_name = fldr.strip()
        if not folder_name:
            logger.warning("Empty folder name provided, skipping.")
            continue

        if folder_name.is_dir():
            logger.info(f"Searching for folders named: {folder_name}")
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
