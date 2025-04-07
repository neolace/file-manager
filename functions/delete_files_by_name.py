import logging
from pathlib import Path
from typing import List


def delete_files_by_name(root_path: Path, filename: str, dry_run: bool = False, logger=None) -> List[Path]:
    if logger is None:
        logger = logging.getLogger(__name__)

    root = Path(root_path)
    files = list(root.rglob(filename))

    count = len(files)
    logger.info(f"Found {count} '{filename}' files")

    deleted_count = 0
    if not dry_run and files:
        for file in files:
            try:
                file.unlink()
                deleted_count += 1
                logger.info(f"Deleted: {file}")
            except PermissionError:
                logger.error(f"Permission denied: {file}")
            except Exception as e:
                logger.error(f"Error deleting {file}: {e}")
        logger.info(f"Removed {deleted_count} '{filename}' files")
    elif dry_run and files:
        for file in files:
            logger.info(f"Would delete: {file}")

    return files
