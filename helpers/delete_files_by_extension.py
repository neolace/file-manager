import logging
from pathlib import Path
from typing import List


def delete_files_by_extension(
    root_path: Path, extension: str, dry_run: bool = False, logger=None
) -> List[Path]:
    if logger is None:
        logger = logging.getLogger(__name__)

    root = Path(root_path)
    files_to_delete = list(root.rglob(f"*.{extension}"))

    count = len(files_to_delete)
    logger.info(f"Found {count} .{extension} files")

    deleted_count = 0
    if not dry_run and files_to_delete:
        for file in files_to_delete:
            try:
                file.unlink()
                deleted_count += 1
                logger.info(f"Deleted: {file}")
            except PermissionError:
                logger.error(f"Permission denied: {file}")
            except Exception as e:
                logger.error(f"Error deleting {file}: {e}")
        logger.info(f"Removed {deleted_count} .{extension} files")
    elif dry_run and files_to_delete:
        for file in files_to_delete:
            logger.info(f"Would delete: {file}")

    return files_to_delete