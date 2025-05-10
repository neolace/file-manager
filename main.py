import logging
from argparse import Namespace
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Dict

from config import settings
from functions.deduplicate import FileDeduplicator
from functions.delete_empty_folders import delete_empty_folders
from functions.process_files import process_files
from functions.remove_folder_by_name import remove_folder_by_name
from utils.parse_arguments import parse_arguments
from utils.setup_logging import setup_logging


class CommandType(Enum):
    """Supported command types"""
    DEDUPLICATE = auto()
    MOVE = auto()
    DELETE_EMPTY = auto()
    REMOVE_FOLDER = auto()


@dataclass
class Command:
    """Represents a command structure with validation and execution handlers."""
    validator: Callable[[Namespace], None]
    handler: Callable[[Namespace, logging.Logger], None]
    description: str


class CommandValidator:
    """Handles validation logic for different commands."""
    @staticmethod
    def validate_deduplicate(args: Namespace) -> None:
        if not args.directory:
            raise ValueError("The 'directory' argument is required for the 'deduplicate' command.")

    @staticmethod
    def validate_move(args: Namespace) -> None:
        if not args.src or not args.dst:
            raise ValueError("Both 'src' and 'dst' arguments are required for the 'move' command.")

    @staticmethod
    def validate_delete_empty_folders(args: Namespace) -> None:
        if not args.src:
            raise ValueError("The 'src' argument is required for the 'delete_empty_folders' command.")

    @staticmethod
    def validate_remove_folder_by_name(args: Namespace) -> None:
        if not args.src or not args.target_name:
            raise ValueError("Both 'src' and 'target_name' arguments are required for the 'remove_folder_by_name' command.")


class CommandHandler:
    """Handles execution of commands"""
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.commands: Dict[str, Command] = self._initialize_commands()

    def _initialize_commands(self) -> Dict[str, Command]:
        return {
            CommandType.DEDUPLICATE.name.lower(): Command(
                CommandValidator.validate_deduplicate,
                lambda args, logger: FileDeduplicator.deduplicate(directory=args.directory, dry_run=args.dry_run),
                "Deduplicate files in directory"
            ),
            CommandType.MOVE.name.lower(): Command(
                CommandValidator.validate_move,
                lambda args, logger: process_files(
                    src_dir=args.src,
                    dst_dir=args.dst,
                    file_types=args.file_types,
                    dry_run=args.dry_run,
                    logger=logger
                ),
                "Move files between directories"
            ),
            CommandType.DELETE_EMPTY.name.lower(): Command(
                CommandValidator.validate_delete_empty_folders,
                lambda args, logger: delete_empty_folders(
                    path=args.src,
                    dry_run=args.dry_run,
                    recursive=args.recursive,
                    logger=logger
                ),
                "Delete empty folders"
            ),
            CommandType.REMOVE_FOLDER.name.lower(): Command(
                CommandValidator.validate_remove_folder_by_name,
                lambda args, logger: remove_folder_by_name(
                    root_path=args.src,
                    target_name=args.target_name,
                    dry_run=args.dry_run,
                    logger=logger
                ),
                "Remove folder by name"
            )
        }

    def execute(self, args: Namespace) -> int:
        """Executes the specified command with given arguments."""
        try:
            if args.command not in self.commands:
                self.logger.error(f"Unsupported command: {args.command}")
                return 1

            command = self.commands[args.command]
            command.validator(args)
            command.handler(args, self.logger)
            self.logger.info("Command executed successfully.")
            return 0
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return 1


def main() -> int:
    args = parse_arguments()
    log_file = Path(args.log or getattr(settings, "DEFAULT_LOG_PATH", "default.log"))
    logger = setup_logging(log_file)

    handler = CommandHandler(logger)
    return handler.execute(args)