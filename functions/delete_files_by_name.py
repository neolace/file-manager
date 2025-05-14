from logging import Logger, getLogger
from pathlib import Path
from typing import List, Optional

DEFAULT_LOGGER = getLogger(__name__)


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
    active_logger = logger or DEFAULT_LOGGER
    target_filenames = prepare_filenames(filenames, case_sensitive)

    try:
        process_directory(
            path, target_filenames, case_sensitive, dry_run, active_logger
        )
    except Exception as e:
        active_logger.error(f"Error accessing {path}: {e}")


def prepare_filenames(filenames: List[str], case_sensitive: bool) -> List[str]:
    """Prepare filenames based on case sensitivity setting."""
    return filenames if case_sensitive else [name.lower() for name in filenames]


def process_directory(
    path: Path,
    target_filenames: List[str],
    case_sensitive: bool,
    dry_run: bool,
    logger: Logger,
) -> None:
    """Process all files in directory and its subdirectories."""
    for item in path.rglob("*"):
        if item.is_file():
            handle_file(item, target_filenames, case_sensitive, dry_run, logger)


def handle_file(
    file_path: Path,
    target_filenames: List[str],
    case_sensitive: bool,
    dry_run: bool,
    logger: Logger,
) -> None:
    """Handle individual file processing and deletion."""
    compare_name = file_path.name if case_sensitive else file_path.name.lower()

    if compare_name in target_filenames:
        if dry_run:
            logger.info(f"Would delete file: {file_path}")
        else:
            delete_file(file_path, logger)


def delete_file(file_path: Path, logger: Logger) -> None:
    """Delete file and handle potential errors."""
    try:
        file_path.unlink()
        logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")
