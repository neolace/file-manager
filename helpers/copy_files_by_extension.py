import shutil
from logging import Logger
from pathlib import Path
from typing import List, Optional


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
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

    extensions = [ext.lower().lstrip(".") for ext in extensions]

    for file_path in source_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower().lstrip(".") in extensions:
            relative_path = file_path.relative_to(source_dir)
            destination_path = destination_dir / relative_path
            if dry_run:
                logger.info(f"Would copy {file_path} to {destination_path}")
            else:
                try:
                    destination_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, destination_path)
                    logger.info(f"Copied {file_path} to {destination_path}")
                except Exception as e:
                    logger.error(
                        f"Error copying {file_path} to {destination_path}: {e}"
                    )
