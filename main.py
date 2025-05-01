"""
File Manager: A utility for managing files and directories.

This module provides functionality to organize, clean, and manage files based on
configurable rules and filters.
"""
import sys
import typing
from pathlib import Path

import pyfiglet

from config import settings
from file_manager.parse_arguments import parse_arguments
from helpers.drop_all_empty_folders import drop_all_empty_folders
from helpers.process_files import process_files
from helpers.remove_folder_by_name import remove_folder_by_name
from helpers.setup_logging import setup_logging


def main(
        dry_run: bool = False,
        src_path: typing.Optional[str] = None,
        dst_path: typing.Optional[str] = None,
        log_path: typing.Optional[str] = None,
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
    src = Path(src_path or settings.DEFAULT_SRC_PATH)
    dst = Path(dst_path or settings.DEFAULT_DST_PATH)
    log_file = Path(log_path or settings.DEFAULT_LOG_PATH)

    # Set up logging
    logger = setup_logging(log_file=log_file)
    logger.info(f"Source: {src}, Destination: {dst}")
    logger.info(f"Dry run mode: {'enabled' if dry_run else 'disabled'}")

    #process_files(
    #        src, dst,
    #        file_types=settings.FILE_TYPES_TO_KEEP,
    #        dry_run=dry_run,
    #        logger=logger
    #        )

    #remove_folder_by_name(src, dry_run=dry_run, logger=logger)

    #drop_all_empty_folders(src, dry_run=dry_run, logger=logger)

    logger.info("File Manager completed.")

    return 0

if __name__ == "__main__":
    figlet = pyfiglet.Figlet(font="slant")
    print(figlet.renderText("FILE-MANAGER"))
    args = parse_arguments()
    EXIT_CODE = main(
            dry_run=args.dry_run, src_path=args.src,
            dst_path=args.dst, log_path=args.log
            )
    sys.exit(EXIT_CODE)
