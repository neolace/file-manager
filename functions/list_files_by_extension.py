import logging
from pathlib import Path
from typing import List


def list_files_by_extension(root_path: Path, file_type: str, logger=None) -> List[Path]:
    """
    List all files with the specified extension in the directory.

    Args:
        root_path: The root directory to search in
        file_type: File extension to search for (without the dot)
        logger: Logger instance for output

    Returns:
        List of Path objects representing the files found
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    root_path = Path(root_path)
    files = list(root_path.rglob(f"*.{file_type}"))

    logger.info(f"Found {len(files)} .{file_type} files")
    for file in files:
        logger.info(f"Found file: {file}")

    return files
