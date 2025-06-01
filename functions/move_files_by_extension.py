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


def _move_file_to_target(source_file_path: Path, target_file_path: Path, logger: logging.Logger) -> bool:
    """
    Moves a single file from source_file_path to target_file_path.
    Logs success or failure using Config messages.
    """
    try:
        shutil.move(source_file_path, target_file_path)
        logger.info(Config.get_log_message("MOVE_SUCCESS").format(source_file_path, target_file_path))
        return True
    except FileNotFoundError:
        msg = f"Source file not found: {source_file_path}"
        logger.error(Config.get_log_message("MOVE_FAILURE").format(source_file_path, target_file_path, msg))
    except PermissionError as pe:
        msg = f"Permission error: {pe}"
        logger.error(Config.get_log_message("MOVE_FAILURE").format(source_file_path, target_file_path, msg))
    except Exception as e:
        logger.error(Config.get_log_message("MOVE_FAILURE").format(source_file_path, target_file_path, str(e)))
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

    if not file_extension:
        logger.error("File extension cannot be empty.")
        return

    # Normalize extension (remove the leading dot if present)
    normalized_extension = file_extension.lstrip(".")

    if not source_folder.exists() or not source_folder.is_dir():
        logger.error(Config.get_log_message("SOURCE_NOT_FOUND").format(source_folder))
        return

    files = find_files(source_folder, normalized_extension)
    logger.info(
        Config.get_log_message("FILES_FOUND").format(len(files), normalized_extension)
    )

    if not files:
        logger.info(f"No .{normalized_extension} files found to move in {source_folder}.")
        return

    if not dry_run:
        try:
            target_folder.mkdir(parents=True, exist_ok=True)
            logger.info(Config.get_log_message("TARGET_CREATED").format(target_folder))
        except OSError as e:
            logger.error(f"Failed to create target directory {target_folder}: {e}")
            return

    moved_count = 0
    for file_path in files:
        unique_target_file_path = get_unique_target_path(target_folder, file_path)

        if dry_run:
            logger.info(Config.get_log_message("WOULD_MOVE").format(file_path, unique_target_file_path))
            moved_count += 1
        else:
            if _move_file_to_target(file_path, unique_target_file_path, logger):
                moved_count += 1

    action = "Would move" if dry_run else "Moved"
    logger.info(
        Config.get_log_message("SUMMARY").format(action, moved_count, normalized_extension)
    )
