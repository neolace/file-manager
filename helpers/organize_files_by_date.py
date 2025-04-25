import datetime
import logging
import shutil
from pathlib import Path


def organize_files_by_date(
    root_path: Path,
    target_folder: Path,
    date_format: str = "%Y-%m",
    use_modified_date: bool = True,
    dry_run: bool = False,
    logger=None,
) -> None:
    if logger is None:
        logger = logging.getLogger(__name__)

    root_path = Path(root_path)
    target_folder = Path(target_folder)

    if not root_path.exists():
        logger.error(f"Source folder does not exist: {root_path}")
        return

    try:
        files = [f for f in root_path.rglob("*") if f.is_file()]
        logger.info(f"Found {len(files)} files to organize")

        if not dry_run and not target_folder.exists():
            target_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created target directory: {target_folder}")

        organized_count = 0
        for file in files:
            if use_modified_date:
                timestamp = datetime.datetime.fromtimestamp(file.stat().st_mtime)
            else:
                timestamp = datetime.datetime.fromtimestamp(file.stat().st_ctime)

            date_folder_name = timestamp.strftime(date_format)
            date_folder_path = target_folder / date_folder_name
            target_path = date_folder_path / file.name

            counter = 1
            while not dry_run and target_path.exists():
                target_path = date_folder_path / f"{file.stem}_{counter}{file.suffix}"
                counter += 1

            if not dry_run:
                if not date_folder_path.exists():
                    date_folder_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created date folder: {date_folder_path}")

                try:
                    shutil.copy2(file, target_path)
                    organized_count += 1
                    logger.info(f"Organized {file} to {target_path}")
                except OSError as e:
                    logger.error(f"Failed to organize {file}: {e}")
            else:
                logger.info(f"Would organize {file} to {date_folder_path / file.name}")

        logger.info(
            f"{'Would organize' if dry_run else 'Organized'} {organized_count} files"
        )

    except OSError as e:
        logger.error(f"Error organizing files by date: {e}")
