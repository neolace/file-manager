import logging
from pathlib import Path
from typing import List, Optional, Protocol

from config.Config import Config
from functions.rename_files_by_extension import rename_files_by_extension


class LoggerProtocol(Protocol):
    def info(self, msg: str) -> None:
        pass

    def error(self, msg: str) -> None:
        pass


def validate_inputs(
        root_path: Path, extensions: List[str], logger: LoggerProtocol
) -> bool:
    """Validate input parameters before processing."""
    if not extensions:
        logger.error(Config.ERROR_NO_EXTENSIONS)
        return False

    if not root_path.exists():
        logger.error(Config.ERROR_PATH_NOT_EXISTS.format(root_path))
        return False

    if not root_path.is_dir():
        logger.error(Config.ERROR_NOT_DIRECTORY.format(root_path))
        return False

    return True


def rename_all_files_by_extensions(
        root_path: Path,
        extensions: List[str],
        dry_run: bool = False,
        logger: Optional[LoggerProtocol] = None,
) -> None:
    """
    Rename all files with specified extensions in the given directory.

    Args:
        root_path: Directory path where files should be renamed
        extensions: List of file extensions to process
        dry_run: If True, only simulate the renaming
        logger: Logger instance for output messages
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    if not validate_inputs(root_path, extensions, logger):
        return

    # Log operation details at once
    logger.info(
        f"Starting rename operation:\n"
        f"- Directory: {root_path}\n"
        f"- Extensions: {extensions}\n"
        f"- Dry run: {dry_run}"
    )

    for extension in extensions:
        rename_files_by_extension(
            directory=root_path,
            extension=extension,
            new_base_name=extension,
            dry_run=dry_run,
            logger=logger,
        )
