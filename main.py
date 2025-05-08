from pathlib import Path
import logging
from typing import Dict, Callable, Any, Optional, List
from config import settings
from functions.deduplicate import deduplicate
from functions.process_files import process_files
from utils.parse_arguments import parse_arguments
from utils.setup_logging import setup_logging


def validate_deduplicate_args(directory: Optional[str]) -> None:
    """Validate arguments for the deduplicate command."""
    if not directory:
        raise ValueError("The 'directory' argument is required for the 'deduplicate' command.")


def validate_move_args(src: Optional[str], dst: Optional[str]) -> None:
    """Validate arguments for the move command."""
    if not src or not dst:
        raise ValueError("Both 'src' and 'dst' arguments are required for the 'move' command.")


def main() -> int:
    """
    Main function to handle command line arguments and execute the appropriate function.
    :return: 0 if successful, 1 if there was an error
    :rtype: int
    """
    args = parse_arguments()
    log_file = Path(args.log or getattr(settings, "DEFAULT_LOG_PATH", "default.log"))
    logger = setup_logging(log_file)

    # Define command handlers
    command_handlers: Dict[str, Callable] = {
        "deduplicate": lambda: handle_deduplicate(args, logger),
        "move": lambda: handle_move(args, logger)
    }

    try:
        # Check if the command is supported
        command = getattr(args, "command", None)
        if command not in command_handlers:
            logger.error(f"Unsupported command: {command}")
            return 1

        # Dispatch to the appropriate command handler
        command_handlers[command]()
        
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


def handle_deduplicate(args: Any, logger: logging.Logger) -> None:
    """Handle the deduplicate command."""
    directory = getattr(args, "directory", None)
    dry_run = getattr(args, "dry_run", False)
    
    validate_deduplicate_args(directory)
    
    deduplicate(
        directory=directory,
        logger=logger,
        dry_run=dry_run
    )


def handle_move(args: Any, logger: logging.Logger) -> None:
    """Handle the move command."""
    src = getattr(args, "src", None)
    dst = getattr(args, "dst", None)
    file_types = getattr(args, "file_types", [])
    dry_run = getattr(args, "dry_run", False)
    
    validate_move_args(src, dst)
    
    process_files(
        src_dir=src,
        dst_dir=dst,
        file_types=file_types,
        dry_run=dry_run,
        logger=logger
    )