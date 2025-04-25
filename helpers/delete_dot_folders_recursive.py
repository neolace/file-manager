import logging
import shutil
from pathlib import Path
from typing import Optional, Union


def delete_dot_folders_recursive(
    root_path: Union[str, Path],
    dry_run: bool = False,
    logger: Optional[logging.Logger] = None,
) -> int:
    """
    Find and remove all folders that start with '.' recursively.

    Args:
        root_path: The root directory to search in
        dry_run: If True, only show what would be deleted without actually deleting
        logger: Logger instance for output

    Returns:
        Number of folders processed
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    root = Path(root_path)
    count = 0

    if not root.exists():
        logger.error(f"Root path does not exist: {root}")
        return 0

    # Find all directories including hidden ones
    dot_folders = [
        folder
        for folder in root.glob("**/*")
        if folder.is_dir() and folder.name.startswith(".")
    ]

    logger.info(f"Found {len(dot_folders)} dot folders under {root}")

    # Sort in reverse order to delete deeper directories first
    for folder in sorted(dot_folders, key=lambda p: str(p), reverse=True):
        count += 1
        if dry_run:
            logger.info(f"Would delete: {folder}")
        else:
            try:
                shutil.rmtree(folder)
                logger.info(f"Deleted folder: {folder}")
            except OSError as e:
                logger.error(f"Error deleting {folder}: {e}")

    logger.info(f"Processed {count} folders starting with '.' under {root}")
    return count
