import logging
import shutil
from pathlib import Path
from typing import Optional, Union


def delete_all_hidden_folders(
    folder_path: Union[str, Path],
    dry_run: bool = False,
    logger: Optional[logging.Logger] = None,
) -> int:
    """
    Delete all hidden folders (starting with '.') in the given directory.

    Args:
        folder_path: Path to the directory to clean
        dry_run: If True, only show what would be deleted without actually deleting
        logger: Logger instance for output

    Returns:
        Number of folders deleted or that would be deleted
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    folder_path = Path(folder_path)

    if not folder_path.exists():
        logger.error(f"Folder does not exist: {folder_path}")
        return 0

    if not folder_path.is_dir():
        logger.error(f"Path is not a directory: {folder_path}")
        return 0

    # Find all hidden folders (starting with '.')
    hidden_folders = [
        item
        for item in folder_path.iterdir()
        if item.is_dir() and item.name.startswith(".")
    ]

    logger.info(f"Found {len(hidden_folders)} hidden folders in {folder_path}")

    deleted_count = 0
    for folder in hidden_folders:
        try:
            if not dry_run:
                shutil.rmtree(folder)
                logger.info(f"Deleted hidden folder: {folder}")
                deleted_count += 1
            else:
                logger.info(f"Would delete hidden folder: {folder}")
                deleted_count += 1
        except Exception as e:
            logger.error(f"Failed to delete {folder}: {e}")

    logger.info(
        f"{'Would delete' if dry_run else 'Deleted'} {deleted_count} hidden folders from {folder_path}"
    )

    return deleted_count
