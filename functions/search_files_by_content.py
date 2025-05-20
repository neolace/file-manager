import logging
import re
from pathlib import Path
from typing import List, Optional
from config import fm_FileType
from config.Config import Config


def search_files_by_content(
    root_path: Path,
    search_text: str,
    file_types: Optional[List[str]] = None,
    case_sensitive: bool = False,
    logger: Optional[logging.Logger] = None,
) -> List[Path]:
    """
    Search for files containing specific text in their content.

    Args:
        root_path: Directory to search in
        search_text: Text to search for
        file_types: List of file extensions to search (default: settings.FILE_TYPES_TO_KEEP)
        case_sensitive: Whether to perform case-sensitive search
        logger: Custom logger instance

    Returns:
        List of Path objects for files containing the search text
    """
    logger = logger or logging.getLogger(__name__)
    root_path = Path(root_path)

    if not root_path.exists():
        raise FileNotFoundError(f"Root path does not exist: {root_path}")
    if not search_text:
        raise ValueError("Search text cannot be empty")

    try:
        matching_files = _find_matching_files(
            root_path=root_path,
            search_text=search_text,
            file_types=file_types or fm_FileType.fm_fileTypeList,
            case_sensitive=case_sensitive,
            logger=logger,
        )
        logger.info(f"Found {len(matching_files)} files containing '{search_text}'")
        return matching_files

    except Exception as e:
        logger.error(f"Error searching files by content: {e}")
        return []


def _find_matching_files(
    root_path: Path,
    search_text: str,
    file_types: List[str],
    case_sensitive: bool,
    logger: logging.Logger,
) -> List[Path]:
    """Find files containing the search text in the given directory."""
    files = _collect_files(root_path, file_types)
    logger.info(f"Found {len(files)} files to search for '{search_text}'")

    pattern = re.compile(search_text, flags=0 if case_sensitive else re.IGNORECASE)
    matching_files = []

    for file in files:
        if _file_contains_pattern(file, pattern, logger):
            matching_files.append(file)
            logger.info(f"Found match in: {file}")

    return matching_files


def _collect_files(root_path: Path, file_types: List[str]) -> List[Path]:
    """Collect all files with specified extensions."""
    files = []
    for extension in file_types:
        files.extend(list(root_path.rglob(f"*.{extension}")))
    return files


def _file_contains_pattern(
    file: Path, pattern: re.Pattern, logger: logging.Logger
) -> bool:
    """Check if a file contains the given pattern."""
    try:
        with open(
            file,
            "r",
            encoding=Config.DEFAULT_ENCODING,
            errors="ignore",
        ) as f:
            return any(pattern.search(line) for line in f)
    except IOError as e:
        logger.error(f"Error reading {file}: {e}")
        return False
