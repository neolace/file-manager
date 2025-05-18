import logging
import subprocess
from pathlib import Path
from typing import Optional

from config.Config import Config


def validate_paths(
    source_folder: Path, seven_zip_path: Path, logger: logging.Logger
) -> bool:
    """Validate that required paths exist."""
    if not seven_zip_path.exists():
        logger.error(f"7-Zip executable not found: {seven_zip_path}")
        return False
    if not source_folder.exists():
        logger.error(f"Source folder not found: {source_folder}")
        return False
    return True


def extract_single_archive(
    archive: Path, output_folder: Path, seven_zip_path: Path, logger: logging.Logger
) -> None:
    """Extract a single 7z archive to the specified output folder."""
    try:
        subprocess.run(
            [
                str(seven_zip_path),
                Config.EXTRACT_CMD,
                str(archive),
                f"-o{output_folder}",
                Config.FORCE_YES_FLAG,
            ],
            check=True,
            capture_output=True,
        )
        logger.info(f"Extracted {archive.name} to {output_folder}")
    except subprocess.SubprocessError as e:
        logger.error(f"Failed to extract {archive}: {e}")


def extract_7z_files_into_folder(
    source_folder: Path, seven_zip_path: Path, logger: Optional[logging.Logger] = None
) -> None:
    """
    Extract all 7z archives from the source folder into separate subfolders.

    Args:
        source_folder: Path to folder containing 7z archives
        seven_zip_path: Path to 7-Zip executable
        logger: Optional logger instance
    """
    logger = logger or logging.getLogger(__name__)
    source_folder = Path(source_folder)
    seven_zip_path = Path(seven_zip_path)

    if not validate_paths(source_folder, seven_zip_path, logger):
        return

    archives = list(source_folder.glob(Config.SEVEN_ZIP_ARCHIVE_EXT))
    logger.info(f"Found {len(archives)} .7z archives to extract")

    for archive in archives:
        output_folder = source_folder / archive.stem
        output_folder.mkdir(exist_ok=True)
        extract_single_archive(archive, output_folder, seven_zip_path, logger)
