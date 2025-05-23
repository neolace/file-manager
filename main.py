import logging
from abc import ABC, abstractmethod
from argparse import Namespace
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Type

from functions.FileDeduplicator import FileDeduplicator
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
        return "Deduplicate files in a directory"

    def validate(self, args: Namespace) -> None:
        if not args.directory:
            raise ValueError(
                "'directory' argument is required for the 'deduplicate' command."
            )

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        deduplicator = FileDeduplicator(
            directory=args.directory,
            max_workers=args.max_workers,
            logger=logger,
            dry_run=args.dry_run,
        )
        deduplicator.deduplicate()


class MoveCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Move files between directories"

    def validate(self, args: Namespace) -> None:
        if not args.src_dir or not args.dst_dir:
            raise ValueError(
                "Both 'src_dir' and 'dst_dir' arguments are required for the 'move' command."
            )

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        return


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
    log_file = Path(args.log)
    # Ensure args.log_level is a string name of the enum member for setup_logging
    logger = setup_logging(log_file=log_file, log_level_str=args.log_level.name)
    handler = CommandHandler(logger)
    return handler.execute(args)


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)

#  python main.py --command "deduplicate" --directory "C:\Users\terti\Downloads\jpeg" --log "app.log" --dry-run
#  python main.py --command "move" --directory "C:\Users\terti\Downloads\jpeg" --log "app.log" --dry-run
