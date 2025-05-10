import shutil
from logging import Logger
from pathlib import Path
from typing import List, Optional

def _setup_default_logger() -> Logger:
    """Create and return a default logger if none is provided."""
    import logging
    return logging.getLogger(__name__)

def _process_single_file(
    file_path: Path,
    source_dir: Path,
    destination_dir: Path,
    dry_run: bool,
    logger: Logger
) -> None:
    """Process a single file copy operation."""
    relative_path = file_path.relative_to(source_dir)
    destination_path = destination_dir / relative_path

    if dry_run:
        logger.info(f"Would copy {file_path} to {destination_path}")
        return

    try:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, destination_path)
        logger.info(f"Copied {file_path} to {destination_path}")
    except OSError as e:
        logger.error(f"Error copying {file_path} to {destination_path}: {e}")

def copy_files_by_extension(
    source_dir: Path,
    destination_dir: Path,
    extensions: List[str],
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Copy files with specific extensions from source to destination directory.
    Args:
        source_dir: Source directory path
        destination_dir: Destination directory path
        extensions: List of file extensions to copy (without dots)
        dry_run: If True, only log actions without copying files
        logger: Logger instance for output
    """
    active_logger = logger or _setup_default_logger()
    normalized_extensions = [ext.lower().lstrip(".") for ext in extensions]

    for file_path in source_dir.rglob("*"):
        is_matching_file = (
            file_path.is_file() and
            file_path.suffix.lower().lstrip(".") in normalized_extensions
        )

        if is_matching_file:
            _process_single_file(
                file_path=file_path,
                source_dir=source_dir,
                destination_dir=destination_dir,
                dry_run=dry_run,
                logger=active_logger
            )