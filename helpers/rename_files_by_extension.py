import logging
from pathlib import Path


def rename_files_by_extension(
    root_path: Path,
    file_type: str,
    new_name: str,
    dry_run: bool = False,
    logger: object = None,
) -> None:
    """
    Rename all files of a specific type in the directory.

    Args:
        root_path: The root directory to search in
        file_type: File extension to search for (without the dot)
        new_name: New name for the files (without extension)
        dry_run: If True, only show what would be renamed without actually renaming
        logger: Logger instance for output
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    root_path = Path(root_path)
    files = list(root_path.rglob(f"*.{file_type}"))
    logger.info(f"Found {len(files)} .{file_type} files to rename")

    renamed_count = 0
    for index, file in enumerate(files, start=1):
        new_file_path = file.parent / f"{new_name}_{index}{file.suffix}"

        if not dry_run:
            try:
                file.rename(new_file_path)
                renamed_count += 1
                logger.info(f"Renamed {file} to {new_file_path}")
            except Exception as e:
                logger.error(f"Failed to rename {file}: {e}")
        else:
            logger.info(f"Would rename {file} to {new_file_path}")

    logger.info(
        f"{'Would rename' if dry_run else 'Renamed'} {renamed_count} .{file_type} files"
    )