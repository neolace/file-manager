import logging
from pathlib import Path


def move_files_by_extension(source_folder: Path, target_folder: Path, file_type: str, dry_run: bool = False,
                            logger=None) -> None:
    """
    Move all files of a specific type from source to target folder.

    Args:
        source_folder: Folder to search for files
        target_folder: Destination folder for found files
        file_type: File extension to search for (without the dot)
        dry_run: If True, only show what would be moved without actually moving
        logger: Logger instance for output
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    source_folder = Path(source_folder)
    target_folder = Path(target_folder)

    if not source_folder.exists():
        logger.error(f"Source folder does not exist: {source_folder}")
        return

    files = list(source_folder.rglob(f"*.{file_type}"))
    logger.info(f"Found {len(files)} .{file_type} files to move")

    if not dry_run and not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created target directory: {target_folder}")

    moved_count = 0
    for file in files:
        target_path = target_folder / file.name

        # Handle filename conflicts
        counter = 1
        while target_path.exists() and not dry_run:
            target_path = target_folder / f"{file.stem}_{counter}{file.suffix}"
            counter += 1

        if not dry_run:
            try:
                file.replace(target_path)
                moved_count += 1
                logger.info(f"Moved {file} to {target_path}")
            except Exception as e:
                logger.error(f"Failed to move {file}: {e}")
        else:
            logger.info(f"Would move {file} to {target_path}")

    logger.info(f"{'Would move' if dry_run else 'Moved'} {moved_count} .{file_type} files")
