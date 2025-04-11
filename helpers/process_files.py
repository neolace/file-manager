import logging
from pathlib import Path

from helpers.move_files_by_extension import move_files_by_extension


def process_files(src: Path, dst: Path, file_types: [], dry_run: bool, logger: logging.Logger) -> None:
    for file_type in file_types:
        dst_combined = dst / file_type
        logger.info(f"Processing file type: {file_type} -> Destination folder: {dst_combined}")
        if not dry_run:
            move_files_by_extension(source_folder=src, target_folder=dst_combined, file_type=file_type, logger=logger,
                                    dry_run=dry_run)
