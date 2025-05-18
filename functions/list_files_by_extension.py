import logging
from pathlib import Path
from typing import List


def _create_default_logger() -> logging.Logger:
    """Create and return a default logger instance."""
    return logging.getLogger(__name__)


def _log_found_files(files: List[Path], extension: str, logger: logging.Logger) -> None:
    """Log information about found files."""
    logger.info(f"Found {len(files)} .{extension} files")
    for file in files:
        logger.info(f"Found file: {file}")


def list_files_by_extension(
    root_path: Path, extension: str, logger: logging.Logger | None = None
) -> List[Path]:
    """
    List all files with the specified extension in the directory.

    Args:
        root_path: The root directory to search in
        extension: File extension to search for (without the dot)
        logger: Logger instance for output

    Returns:
        List of Path objects representing the files found

    Raises:
        ValueError: If root_path doesn't exist or the extension is empty
    """
    if not extension:
        raise ValueError("Extension cannot be empty")

    root_path = Path(root_path)
    if not root_path.exists():
        raise ValueError(f"Directory does not exist: {root_path}")

    logger = logger or _create_default_logger()
    file_pattern = f"*.{extension}"
    files = list(root_path.rglob(file_pattern))

    _log_found_files(files, extension, logger)
    return files
