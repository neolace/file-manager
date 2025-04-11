import logging
import shutil
from pathlib import Path


def copy_files_by_extension(source_folder: Path, target_folder: Path, file_type: str, dry_run: bool = False,
                            logger=None) -> None:
    if logger is None:
        logger = logging.getLogger(__name__)

    source_folder = Path(source_folder)
    target_folder = Path(target_folder)

    if not source_folder.exists():
        logger.error(f"Source folder does not exist: {source_folder}")
        return

    files = list(source_folder.rglob(f"*.{file_type}"))
    logger.info(f"Found {len(files)} .{file_type} files to copy")

    if not dry_run and not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created target directory: {target_folder}")

    copied_count = 0
    for file in files:
        target_path = target_folder / file.name

        counter = 1
        while target_path.exists() and not dry_run:
            target_path = target_folder / f"{file.stem}_{counter}{file.suffix}"
            counter += 1

        if not dry_run:
            try:
                shutil.copy2(file, target_path)
                copied_count += 1
                logger.info(f"Copied {file} to {target_path}")
            except Exception as e:
                logger.error(f"Failed to copy {file}: {e}")
        else:
            logger.info(f"Would copy {file} to {target_path}")

    logger.info(f"{'Would copy' if dry_run else 'Copied'} {copied_count} .{file_type} files")
