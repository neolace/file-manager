import logging
import shutil
from pathlib import Path


def delete_all_hidden_folders(folder_path: Path, dry_run: bool = False, logger=None) -> None:
    if logger is None:
        logger = logging.getLogger(__name__)

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

    logger.info(f"{'Would delete' if dry_run else 'Deleted'} {deleted_count} items from {folder_path}")
