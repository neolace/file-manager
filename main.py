"""
File Manager: A utility for managing files and directories.

This module provides functionality to organize, clean, and manage files based on
configurable rules and filters.
"""

import pathlib
from typing import Optional

from config import (
    FILE_TYPES_TO_KEEP,
    DEFAULT_SRC_PATH,
    DEFAULT_DST_PATH,
    DEFAULT_LOG_PATH,
)
from helpers.drop_all_empty_folders import drop_all_empty_folders
from helpers.process_files import process_files
from helpers.remove_folder_by_name import remove_folder_by_name
from helpers.setup_logging import setup_logging


def main(
    dry_run: bool = False,
    src_path: Optional[str] = None,
    dst_path: Optional[str] = None,
    log_path: Optional[str] = None,
) -> int:
    """
    Main function to manage files and folders.

    Args:
        dry_run: If True, perform a dry run without making changes
        src_path: Source directory path
        dst_path: Destination directory path
        log_path: Log file path

    Returns:
        Exit code (0 for success)
    """
    # Use defaults if paths not provided
    src = pathlib.Path(src_path or DEFAULT_SRC_PATH)
    dst = pathlib.Path(dst_path or DEFAULT_DST_PATH)
    log_file = pathlib.Path(log_path or DEFAULT_LOG_PATH)

    # Set up logging
    logger = setup_logging(log_file=log_file)
    logger.info(f"Source: {src}, Destination: {dst}")
    logger.info(f"Dry run mode: {'enabled' if dry_run else 'disabled'}")

    process_files(
        src, dst, file_types=FILE_TYPES_TO_KEEP, dry_run=dry_run, logger=logger
    )

    remove_folder_by_name(src, dry_run=dry_run, logger=logger)

    drop_all_empty_folders(src, dry_run=dry_run, logger=logger)

    logger.info("File Manager completed.")

    return 0


import sys

from parse_arguments import parse_arguments

if __name__ == "__main__":
    args = parse_arguments()
    exit_code = main(
        dry_run=args.dry_run, src_path=args.src, dst_path=args.dst, log_path=args.log
    )
    sys.exit(exit_code)
