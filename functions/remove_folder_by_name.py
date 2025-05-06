from logging import Logger
from pathlib import Path
from typing import Optional

from functions.delete_all_files_folders_within_folder import delete_all_files_folders_within_folder


def remove_folder_by_name(root_path: Path,
                          dry_run: bool = False,
                          logger: Optional[Logger] = None,
                          target_name=None) -> None:
    """
    Remove all folders with a specific name within a given root path.
    :param target_name:
    :param root_path:
    :param dry_run:
    :param logger:
    :return:
    """

    root = Path(root_path)
    if not root.exists():
        logger.error(f"Root path does not exist: {root}")
        return

    folders = list(root.rglob("*"))
    for folder in folders:
        if folder.is_dir() and folder.name == target_name:
            if dry_run:
                logger.info(f"Would delete: {folder}")
            else:
                try:
                    delete_all_files_folders_within_folder(folder)
                    logger.info(f"Deleted contents of: {folder}")
                except OSError as e:
                    logger.error(f"Error deleting {folder}: {e}")