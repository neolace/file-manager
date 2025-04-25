from logging import Logger
from pathlib import Path
from typing import List, Optional


def delete_files_by_name(
    path: Path,
    filenames: List[str],
    case_sensitive: bool = False,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Delete all files with the specified names in the given path.

    Args:
        path: The directory path to search for files
        filenames: List of filenames to delete
        case_sensitive: If True, match filenames case-sensitively
        dry_run: If True, only log actions without deleting files
        logger: Logger instance for output
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    names_to_delete = (
        filenames if case_sensitive else [name.lower() for name in filenames]
    )

    try:
        for item in path.rglob("*"):
            if item.is_file():
                compare_name = item.name if case_sensitive else item.name.lower()
                if compare_name in names_to_delete:
                    if dry_run:
                        logger.info(f"Would delete file: {item}")
                    else:
                        try:
                            item.unlink()
                            logger.info(f"Deleted file: {item}")
                        except Exception as e:
                            logger.error(f"Error deleting file {item}: {e}")
    except Exception as e:
        logger.error(f"Error accessing {path}: {e}")
