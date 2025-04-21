import shutil
from logging import getLogger
from pathlib import Path


def delete_all_files_folders_within_folder(
    folder_path: Path, dry_run: bool = False, logger: object = None
) -> None:
    """
    Delete all files and folders within the specified folder without removing the folder itself.

    Args:
        folder_path: Path to the folder whose contents should be deleted
        dry_run: If True, only show what would be deleted without actually deleting
        logger: Logger instance for output
    """
    if logger is None:
        logger = getLogger(__name__)

    folder_path = Path(folder_path)

    if not folder_path.exists():
        logger.error(f"Folder does not exist: {folder_path}")
        return

    if not folder_path.is_dir():
        logger.error(f"Path is not a directory: {folder_path}")
        return

    # Count items for reporting
    items = list(folder_path.iterdir())
    logger.info(f"Found {len(items)} items to delete in {folder_path}")

    deleted_count = 0
    for item in items:
        try:
            if not dry_run:
                if item.is_file():
                    item.unlink()
                    logger.info(f"Deleted file: {item}")
                else:
                    shutil.rmtree(item)
                    logger.info(f"Deleted directory: {item}")
                deleted_count += 1
            else:
                item_type = "file" if item.is_file() else "directory"
                logger.info(f"Would delete {item_type}: {item}")
                deleted_count += 1
        except Exception as e:
            logger.error(f"Failed to delete {item}: {e}")

    logger.info(
        f"{'Would delete' if dry_run else 'Deleted'} {deleted_count} items from {folder_path}"
    )
