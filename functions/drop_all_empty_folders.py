from dataclasses import dataclass
from logging import Logger, getLogger
from pathlib import Path
from typing import Optional, List


@dataclass
class FolderCleanupConfig:
    path: Path
    dry_run: bool = False
    logger: Optional[Logger] = None

    def __post_init__(self):
        if self.logger is None:
            self.logger = getLogger(__name__)


def drop_all_empty_folders(
    path: Path,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Recursively find and delete all empty folders within the given path.
    Continues iterating until no more empty folders can be found.
    Args:
        path: The directory path to start cleaning
        dry_run: If True, only log actions without deleting folders
        logger: Logger instance for output
    """
    config = FolderCleanupConfig(path, dry_run, logger)

    if not _is_valid_directory(config.path, config.logger):
        return

    while _process_empty_folders(config):
        continue


def _is_valid_directory(path: Path, logger: Logger) -> bool:
    """Check if the given path is a valid directory."""
    if path.exists() and path.is_dir():
        return True
    logger.warning(f"Path does not exist or is not a directory: {path}")
    return False


def _get_sorted_directories(base_path: Path) -> List[Path]:
    """Get all directories sorted by depth (deepest first)."""
    directories = [d for d in base_path.rglob("*") if d.is_dir()]
    return sorted(directories, key=lambda x: len(x.parts), reverse=True)


def _process_empty_folders(config: FolderCleanupConfig) -> bool:
    """Process and delete empty folders. Returns True if any folder was deleted."""
    any_folder_deleted = False

    for folder in _get_sorted_directories(config.path):
        if _is_empty_folder(folder):
            if _delete_folder(folder, config):
                any_folder_deleted = True

    return any_folder_deleted


def _is_empty_folder(folder: Path) -> bool:
    """Check if the folder is empty."""
    try:
        return not any(folder.iterdir())
    except OSError:
        return False


def _delete_folder(folder: Path, config: FolderCleanupConfig) -> bool:
    """Delete the folder if not in dry run mode. Returns True if the folder was deleted."""
    try:
        if config.dry_run:
            config.logger.info(f"Would delete empty folder: {folder}")
            return False

        folder.rmdir()
        config.logger.info(f"Deleted empty folder: {folder}")
        return True

    except OSError as e:
        config.logger.error(f"Error processing folder {folder}: {e}")
        return False
