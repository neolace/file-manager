import logging
from pathlib import Path
from typing import List

from functions.rename_files_by_extension import rename_files_by_extension


def rename_all_files_by_extensions(root_path: Path, extensions: List[str], dry_run: bool = False, logger=None) -> None:
    if logger is None:
        logger = logging.getLogger(__name__)

    if extensions is None or len(extensions) == 0:
        logger.error("No file extensions provided.")
        return
    if not root_path.exists():
        logger.error(f"Root path does not exist: {root_path}")
        return
    if not root_path.is_dir():
        logger.error(f"Root path is not a directory: {root_path}")
        return
    logger.info(f"Renaming files in {root_path} for extensions: {extensions}")
    logger.info(f"Root path: {root_path}")
    logger.info(f"Extensions: {extensions}")
    logger.info(f"Dry run: {dry_run}")
    logger.info(f"Logger: {logger}")
    logger.info(f"Extensions: {extensions}")

    for old_extension in extensions:
        rename_files_by_extension(root_path, file_type=old_extension, dry_run=dry_run, logger=logger,
                                  new_name=old_extension)
