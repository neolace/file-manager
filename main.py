import logging
from abc import ABC, abstractmethod
from argparse import Namespace
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Type

from config import settings
from functions.deduplicate import FileDeduplicator
from functions.process_files import process_files
from utils.parse_arguments import parse_arguments
from utils.setup_logging import setup_logging


class CommandType(Enum):
    """Supported command types"""
    DEDUPLICATE = auto()
    MOVE = auto()
    DELETE_EMPTY = auto()
    REMOVE_FOLDER = auto()


class CommandInterface(ABC):
    """Base interface for all commands"""

    @abstractmethod
    def validate(self, args: Namespace) -> None:
        """Validate command arguments"""
        pass

    @abstractmethod
    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        """Execute the command"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Command description"""
        pass


class DeduplicateCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Deduplicate files in directory"

    def validate(self, args: Namespace) -> None:
        if not args.directory:
            raise ValueError("The 'directory' argument is required for the 'deduplicate' command.")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        FileDeduplicator.deduplicate(directory=args.directory, dry_run=args.dry_run)


class MoveCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Move files between directories"

    def validate(self, args: Namespace) -> None:
        if not args.src or not args.dst:
            raise ValueError("Both 'src' and 'dst' arguments are required for the 'move' command.")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        process_files(
            src_dir=args.src,
            dst_dir=args.dst,
            file_types=args.file_types,
            dry_run=args.dry_run,
            logger=logger,
        )


class CommandRegistry:
    """Registry for available commands"""

    def __init__(self):
        self._commands: Dict[str, Type[CommandInterface]] = {
            CommandType.DEDUPLICATE.name.lower(): DeduplicateCommand,
            CommandType.MOVE.name.lower(): MoveCommand,
            # Add other commands similarly
        }

    def get_command(self, command_name: str) -> CommandInterface:
        command_class = self._commands.get(command_name.lower())
        if not command_class:
            raise ValueError(f"Unsupported command: {command_name}")
        return command_class()


class CommandHandler:
    """Handles execution of commands"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.registry = CommandRegistry()

    def execute(self, args: Namespace) -> int:
        """Executes the specified command with given arguments."""
        try:
            command = self.registry.get_command(args.command)
            command.validate(args)
            command.execute(args, self.logger)
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