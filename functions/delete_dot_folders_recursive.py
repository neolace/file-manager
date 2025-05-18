import shutil
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import List, Optional, Sequence

from config.Config import Config

PathSequence = Sequence[Path]


@dataclass
class DeletionConfig:
    """Configuration for a folder deletion process"""

    excluded_names: List[str]
    dry_run: bool
    logger: Logger


def find_dot_folders(root_path: Path, excluded_names: List[str]) -> PathSequence:
    """
    Find all dot folders in the given path, excluding specified names.

    Args:
        root_path: The path to start searching for dot folders
        excluded_names: List of folder names to exclude from results

    Returns:
        Sequence of paths sorted by depth (deepest first)
    """
    dot_folders = [
        item
        for item in root_path.rglob("*")
        if item.is_dir()
        and item.name.startswith(Config.HIDDEN_PREFIX)
        and item.name not in excluded_names
    ]
    return sorted(dot_folders, key=lambda x: len(x.parts), reverse=True)


def delete_folder(folder: Path, config: DeletionConfig) -> None:
    """
    Delete a single folder with logging.

    Args:
        folder: The folder to delete
        config: Deletion configuration
    """
    if config.dry_run:
        config.logger.info(f"Would delete dot folder: {folder}")
        return

    try:
        shutil.rmtree(folder)
        config.logger.info(f"Deleted dot folder: {folder}")
    except OSError as e:
        config.logger.error(f"Error deleting dot folder {folder}: {e}")


def delete_dot_folders_recursive(
    root_path: Path,
    excluded_names: Optional[List[str]] = None,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Recursively find and delete folders that start with a dot (hidden folders).

    Args:
        root_path: The path to start searching for dot folders
        excluded_names: List of folder names to exclude from deletion
        dry_run: If True, only log actions without deleting anything
        logger: Logger instance for output
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    config = DeletionConfig(
        excluded_names=excluded_names or [], dry_run=dry_run, logger=logger
    )

    try:
        dot_folders = find_dot_folders(root_path, config.excluded_names)
        for folder in dot_folders:
            delete_folder(folder, config)
    except OSError as e:
        logger.error(f"Error accessing {root_path}: {e}")
