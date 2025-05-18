import logging
import shutil
from pathlib import Path
from typing import List, Optional

from config.Config import Config


def find_files(source_dir: Path, extension: str) -> List[Path]:
    """Find all files with given extension in source directory."""
    return list(source_dir.rglob(f"*.{extension}"))


def get_unique_target_path(target_dir: Path, source_file: Path) -> Path:
    """Generate a unique target path for a file to avoid naming conflicts."""
    target_path = target_dir / source_file.name
    counter = 1

    while target_path.exists():
        target_path = target_dir / f"{source_file.stem}_{counter}{source_file.suffix}"
        counter += 1

    return target_path


def move_file(source_file: Path, target_path: Path, logger: logging.Logger) -> bool:
    """Move a single file to a target path and handle errors."""
    try:
        shutil.move(source_file, target_path)
        logger.info(
            Config.get_log_message("MOVE_SUCCESS").format(source_file, target_path)
        )
        return True
    except Exception as e:
        logger.error(
            Config.get_log_message("MOVE_FAILURE").format(source_file, target_path, e)
        )
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
        logger.error(Config.get_log_message("SOURCE_NOT_FOUND").format(source_folder))
        return

    files = find_files(source_folder, file_extension)
    logger.info(
        Config.get_log_message("FILES_FOUND").format(len(files), file_extension)
    )

    if not dry_run and not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        logger.info(Config.get_log_message("TARGET_CREATED").format(target_folder))

    moved_count = 0
    for file in files:
        target_path = get_unique_target_path(target_folder, file)

        if dry_run:
            logger.info(Config.get_log_message("WOULD_MOVE").format(file, target_path))
            moved_count += 1
        elif move_file(file, target_path, logger):
            moved_count += 1

    action = "Would move" if dry_run else "Moved"
    logger.info(
        Config.get_log_message("SUMMARY").format(action, moved_count, file_extension)
    )
