import logging
import subprocess
from pathlib import Path


def extract_7z_files_into_folder(
    source_folder: Path, seven_zip_path: Path, logger=None
) -> None:
    if logger is None:
        logger = logging.getLogger(__name__)

    source_folder = Path(source_folder)
    seven_zip_path = Path(seven_zip_path)

    if not seven_zip_path.exists():
        logger.error(f"7-Zip executable not found: {seven_zip_path}")
        return

    archives = list(source_folder.glob("*.7z"))
    logger.info(f"Found {len(archives)} .7z archives to extract")

    for archive in archives:
        output_folder = source_folder / archive.stem
        output_folder.mkdir(exist_ok=True)

        try:
            subprocess.run(
                [str(seven_zip_path), "x", str(archive), f"-o{output_folder}", "-y"],
                check=True,
                capture_output=True,
            )
            logger.info(f"Extracted {archive.name} to {output_folder}")
        except subprocess.SubprocessError as e:
            logger.error(f"Failed to extract {archive}: {e}")