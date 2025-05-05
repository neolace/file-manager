"""
File Manager: A utility for managing files and directories.

This module provides functionality to organize, clean, and manage files based on
configurable rules and filters.
"""
from functools import lru_cache
from pathlib import Path

import pyfiglet

from config import settings
from functions.deduplicate import deduplicate
from functions.parse_arguments import parse_arguments
from functions.setup_logging import setup_logging


@lru_cache(maxsize=1)
def get_figlet():
    return pyfiglet.Figlet(font=settings.DEFAULT_FONT)


def main(args) -> int:
    """
    Main function to manage files and folders.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success)
    """
    # Use defaults if paths not provided
    src = args.src and Path(args.src) or Path(settings.DEFAULT_SRC_PATH)
    dst = args.dst and Path(args.dst) or Path(settings.DEFAULT_DST_PATH)
    log_file = args.log and Path(args.log) or Path(settings.DEFAULT_LOG_PATH)

    if args.command == "deduplicate":
        deduplicate(directory=args.path, dry_run=args.dry_run)

    # Set up logging
    logger = setup_logging(log_file=log_file)
    logger.info(f"Source: {src}, Destination: {dst}, Dry run mode: {'enabled' if args.dry_run else 'disabled'}")

    logger.info("File Manager completed.")

    return 0


if __name__ == "__main__":
    figlet = get_figlet()
    print(figlet.renderText("FILE-MANAGER"))
    args = parse_arguments()
    exit(main(args=args))