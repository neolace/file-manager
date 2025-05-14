import logging
import shutil
from pathlib import Path
from typing import List, Optional

# Constants for log messages
LOG_MESSAGES = {
    "SOURCE_NOT_FOUND": "Source folder does not exist: {}",
    "FILES_FOUND": "Found {} .{} files to move",
    "TARGET_CREATED": "Created target directory: {}",
    "MOVE_SUCCESS": "Moved {} to {}",
    "MOVE_FAILURE": "Failed to move {} to {}: {}",
    "WOULD_MOVE": "Would move {} to {}",
    "SUMMARY": "{} {} .{} files",
}


def find_files(source_dir: Path, extension: str) -> List[Path]:
    """Find all files with given extension in source directory."""
    return list(source_dir.rglob(f"*.{extension}"))


def get_unique_target_path(target_dir: Path, source_file: Path) -> Path:
    """Generate unique target path for file to avoid naming conflicts."""
    target_path = target_dir / source_file.name
    counter = 1

    while target_path.exists():
        target_path = target_dir / f"{source_file.stem}_{counter}{source_file.suffix}"
        counter += 1

    return target_path


def move_file(source_file: Path, target_path: Path, logger: logging.Logger) -> bool:
    """Move single file to target path and handle errors."""
    try:
        shutil.move(source_file, target_path)
        logger.info(LOG_MESSAGES["MOVE_SUCCESS"].format(source_file, target_path))
        return True
    except Exception as e:
        logger.error(LOG_MESSAGES["MOVE_FAILURE"].format(source_file, target_path, e))
        return False


def move_files_by_extension(
    source_folder: Path,
    target_folder: Path,
    file_extension: str,
    dry_run: bool = False,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Move all files with specified extension from source to target folder."""
    logger = logger or logging.getLogger(__name__)
    source_folder = Path(source_folder)
    target_folder = Path(target_folder)

    if not source_folder.exists():
        logger.error(LOG_MESSAGES["SOURCE_NOT_FOUND"].format(source_folder))
        return

    files = find_files(source_folder, file_extension)
    logger.info(LOG_MESSAGES["FILES_FOUND"].format(len(files), file_extension))

    if not dry_run and not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        logger.info(LOG_MESSAGES["TARGET_CREATED"].format(target_folder))

    moved_count = 0
    for file in files:
        target_path = get_unique_target_path(target_folder, file)

        if dry_run:
            logger.info(LOG_MESSAGES["WOULD_MOVE"].format(file, target_path))
            moved_count += 1
        elif move_file(file, target_path, logger):
            moved_count += 1

    action = "Would move" if dry_run else "Moved"
    logger.info(LOG_MESSAGES["SUMMARY"].format(action, moved_count, file_extension))
