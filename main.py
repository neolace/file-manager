from pathlib import Path

from config import settings
from functions.deduplicate import deduplicate
from functions.process_files import process_files
from utils.parse_arguments import parse_arguments
from utils.setup_logging import setup_logging


def main() -> int:
    """
    Main function to handle command line arguments and execute the appropriate function.

    :return:
    """
    args = parse_arguments()
    log_file = Path(args.log or getattr(settings, "DEFAULT_LOG_PATH", "default.log"))
    logger = setup_logging(log_file)
    try:

        args.log = getattr(args, "log", None)
        args.command = getattr(args, "command", None)
        args.directory = getattr(args, "directory", None)
        args.src = getattr(args, "src", None)
        args.dst = getattr(args, "dst", None)
        args.file_types = getattr(args, "file_types", [])
        args.dry_run = getattr(args, "dry_run", False)


        logger = setup_logging(log_file)

        if args.command == "deduplicate":
            if not args.directory:
                raise ValueError("The 'directory' argument is required for the 'deduplicate' command.")
            deduplicate(
                directory=args.directory,
                logger=logger,
                dry_run=args.dry_run
            )
        elif args.command == "move":
            if not args.src or not args.dst:
                raise ValueError("Both 'src' and 'dst' arguments are required for the 'move' command.")
            process_files(
                src_dir=args.src,
                dst_dir=args.dst,
                file_types=args.file_types,
                dry_run=args.dry_run,
                logger=logger
            )
        else:
            logger.error(f"Unsupported command: {args.command}")
            return 1

        logger.info("File Manager completed.")
        return 0

    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return 1
    except FileNotFoundError as fnfe:
        logger.error(f"FileNotFoundError: {fnfe}")
        return 1
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return 1