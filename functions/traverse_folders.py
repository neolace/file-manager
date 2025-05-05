import logging
from pathlib import Path


def traverse_folders(path, logger=None, dry_run=True):
    """
    Recursively loop through all folders and subfolders starting from the given path.
    Default path is the current working directory.
    
    Args:
        path: The directory path to traverse
        logger: Logger instance to use (creates one if None)
        dry_run: If True, only log actions without making changes
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    path = Path(path) if not isinstance(path, Path) else path

    # Iterate through all items in the current path
    for item in path.iterdir():
        # Check if the item is a directory
        if item.is_dir():
            logger.info(f"Found folder: {item}")
            
            # Only process folders that are not hidden (don't start with dot)
            if not item.name.startswith('.'):
                # Recursively traverse the subdirectory
                traverse_folders(item, logger, dry_run)
