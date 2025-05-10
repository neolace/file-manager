import logging
import shutil
from pathlib import Path

_logger = logging.getLogger(__name__)

def process_files(src_dir: str, dst_dir: str, file_types: list, dry_run: bool, logger: _logger) -> None:

    """
    Process files from source directory to destination directory based on file types.

    Args:
        src_dir: Source directory path
        dst_dir: Destination directory path
        file_types: List of file extensions to process (without dots)
        dry_run: If True, only log actions without moving files
        logger: Logger instance for output
    """
    logger.info(f"Processing files from {src_dir} to {dst_dir}")

    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    normalized_file_types = [ft.lower().lstrip(".") for ft in file_types]

    try:
        for file_path in src_dir.rglob("*"):
            if (
                file_path.is_file()
                and file_path.suffix.lower().lstrip(".") in normalized_file_types
            ):
                rel_path = file_path.relative_to(src_dir)
                target_file = dst_dir / rel_path
                if not dry_run:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                if (
                    not target_file.exists()
                    or file_path.stat().st_mtime > target_file.stat().st_mtime
                ):
                    if dry_run:
                        logger.info(f"Would copy {file_path} to {target_file}")
                    else:
                        try:
                            shutil.copy2(file_path, target_file)
                            logger.info(f"Copied {file_path} to {target_file}")
                        except OSError as e:
                            logger.error(f"Error copying {file_path}: {e}")
    except OSError as e:
        logger.error(f"Error processing files: {e}")

    logger.info("File processing completed.")