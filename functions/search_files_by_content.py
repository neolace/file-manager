import logging
import re
from pathlib import Path
from typing import List

from dill import settings


def search_files_by_content(
    root_path: Path,
    search_text: str,
    file_types: List[str] = None,
    case_sensitive: bool = False,
    logger=None,
) -> List[Path]:
    if logger is None:
        logger = logging.getLogger(__name__)

    root_path = Path(root_path)
    matched_files = []

    extensions = file_types if file_types else settings.FILE_TYPES_TO_KEEP

    try:
        files = []
        for ext in extensions:
            files.extend(list(root_path.rglob(f"*.{ext}")))

        logger.info(f"Found {len(files)} files to search for '{search_text}'")

        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(search_text, flags)

        for file in files:
            try:
                with open(file, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if pattern.search(line):
                            matched_files.append(file)
                            logger.info(f"Found match in: {file}")
                            break
            except Exception as e:
                logger.error(f"Error searching {file}: {e}")

        logger.info(f"Found {len(matched_files)} files containing '{search_text}'")

    except Exception as e:
        logger.error(f"Error searching files by content: {e}")

    return matched_files
