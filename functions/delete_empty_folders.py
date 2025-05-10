from logging import Logger
from pathlib import Path
from typing import Optional


def delete_empty_folders(
    path: Path,
    dry_run: bool = False,
    recursive: bool = True,
    logger: Optional[Logger] = None,
) -> int:
    """
    Delete empty folders starting from the given path.
    
    Args:
        path: The directory path to start cleaning
        dry_run: If True, only simulate deletion and log actions
        recursive: If True, keep scanning until no more empty folders are found
        logger: Logger instance for output
    
    Returns:
        int: Number of folders deleted (or would be deleted in dry_run mode)
    
    Raises:
        ValueError: If the path doesn't exist or is not a directory
    """
    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    if not path.exists() or not path.is_dir():
        raise ValueError(f"Path does not exist or is not a directory: {path}")

    deleted_count = 0
    
    def _delete_folder(folder: Path) -> bool:
        """Helper function to delete a single folder if empty."""
        try:
            if not any(folder.iterdir()):
                if dry_run:
                    logger.info(f"Would delete empty folder: {folder}")
                else:
                    folder.rmdir()
                    logger.info(f"Deleted empty folder: {folder}")
                return True
        except PermissionError:
            logger.error(f"Permission denied accessing folder: {folder}")
        except OSError as e:
            logger.error(f"Error processing folder {folder}: {e}")
        return False

    while True:
        folders_deleted = 0
        # Sort by depth (deepest first) to handle nested empty folders efficiently
        dirs = sorted(
            [d for d in path.rglob("*") if d.is_dir()],
            key=lambda x: len(x.parts),
            reverse=True
        )
        
        for folder in dirs:
            if _delete_folder(folder):
                folders_deleted += 1
                
        deleted_count += folders_deleted
        
        # If not recursive or no folders were deleted this round, break
        if not recursive or folders_deleted == 0:
            break

    return deleted_count