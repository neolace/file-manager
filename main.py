import argparse
import logging
from pathlib import Path

from config import settings
from functions.deduplicate import deduplicate


def setup_logging(log_file: Path) -> logging.Logger:
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("file_manager")

def get_path(arg_path, default_path):
    return Path(arg_path) if arg_path else Path(default_path)

def parse_arguments():
    parser = argparse.ArgumentParser(description="File Manager Tool")
    parser.add_argument("--src", help="Source directory path")
    parser.add_argument("--dst", help="Destination directory path")
    parser.add_argument("--log", help="Log file path")
    parser.add_argument("--dry-run", action="store_true", help="Run without making changes")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Deduplicate command
    dedup_parser = subparsers.add_parser("deduplicate", help="Remove duplicate files")
    dedup_parser.add_argument("path", help="Directory path to deduplicate")
    
    return parser.parse_args()

def main() -> int:
    args = parse_arguments()
    src = get_path(args.src, settings.DEFAULT_SRC_PATH)
    dst = get_path(args.dst, settings.DEFAULT_DST_PATH)
    log_file = get_path(args.log, settings.DEFAULT_LOG_PATH)

    logger = setup_logging(log_file=log_file)
    logger.info(f"Source: {src}, Destination: {dst}, Dry run mode: {'enabled' if args.dry_run else 'disabled'}")

    if args.command == "deduplicate":
        deduplicate(directory=args.path, dry_run=args.dry_run)

    logger.info("File Manager completed.")
    return 0

if __name__ == "__main__":
    exit(main())
