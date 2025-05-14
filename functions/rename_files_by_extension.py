import logging
from pathlib import Path
from typing import List, Optional, Protocol


class LoggerProtocol(Protocol):
    def info(self, msg: str) -> None: ...
    def error(self, msg: str) -> None: ...


def find_files_by_extension(directory: Path, extension: str) -> List[Path]:
    """Find all files with given extension in directory and subdirectories."""
    return list(directory.rglob(f"*.{extension}"))


def generate_new_filename(original_file: Path, base_name: str, index: int) -> Path:
    """Generate new file path with indexed name."""
    return original_file.parent / f"{base_name}_{index}{original_file.suffix}"


def rename_single_file(file: Path, new_path: Path, logger: LoggerProtocol) -> bool:
    """Rename single file and handle errors. Returns True if successful."""
    try:
        file.rename(new_path)
        logger.info(f"Renamed {file} to {new_path}")
        return True
    except OSError as e:
        logger.error(f"Failed to rename {file}: {e}")
        return False


def rename_files_by_extension(
    directory: Path,
    extension: str,
    new_base_name: str,
    dry_run: bool = False,
    logger: Optional[LoggerProtocol] = None,
) -> None:
    """
    Rename all files of a specific type in the directory.

    Args:
        directory: The root directory to search in
        extension: File extension to search for (without the dot)
        new_base_name: New base name for the files (without extension)
        dry_run: If True, only show what would be renamed without actually renaming
        logger: Logger instance for output
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    directory = Path(directory)
    files = find_files_by_extension(directory, extension)
    logger.info(f"Found {len(files)} .{extension} files to rename")

    renamed_count = 0
    for index, file in enumerate(files, start=1):
        new_file_path = generate_new_filename(file, new_base_name, index)

        if dry_run:
            logger.info(f"Would rename {file} to {new_file_path}")
            continue

        if rename_single_file(file, new_file_path, logger):
            renamed_count += 1

    action = "Would rename" if dry_run else "Renamed"
    logger.info(f"{action} {renamed_count} .{extension} files")
