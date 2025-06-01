import logging
from argparse import Namespace
from pathlib import Path
from typing import Dict, Type

from Interface import CommandInterface
from utils.parse_arguments import parse_arguments
from utils.setup_logging import setup_logging
from functions import CommandType, DeduplicateCommand, DeleteHiddenFilesCommand, DeleteByExtensionCommand, MoveCommand, CleanFolderCommand, DeleteEmptyFoldersCommand, RenameFilesCommand, CompressFilesCommand


class CommandRegistry:
    """Registry for available commands"""

    def __init__(self):
        self._commands: Dict[str, Type[CommandInterface]] = {
            CommandType.DEDUPLICATE.name.lower(): DeduplicateCommand,
            CommandType.MOVE.name.lower(): MoveCommand,
            CommandType.DELETE_BY_EXTENSION.name.lower(): DeleteByExtensionCommand,
            CommandType.CLEAN_FOLDER.name.lower(): CleanFolderCommand,
            CommandType.DELETE_EMPTY.name.lower(): DeleteEmptyFoldersCommand,
            CommandType.DELETE_HIDDEN_FILES.name.lower(): DeleteHiddenFilesCommand,
            "rename_files": RenameFilesCommand,
            "compress_files": CompressFilesCommand,
        }

    def get_command(self, command_name: str) -> CommandInterface:
        command_class = self._commands.get(command_name.lower())
        if not command_class:
            valid_commands = ", ".join(self._commands.keys())
            raise ValueError(f"Unsupported command: {command_name}. Supported commands are: {valid_commands}")
        return command_class()


class CommandHandler:
    """Handles execution of commands"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.registry = CommandRegistry()

    def execute(self, args: Namespace) -> int:
        try:
            command_name = args.command.lower()
            command = self.registry.get_command(command_name)
            command.validate(args)
            command.execute(args, self.logger)
            self.logger.info(f"Command '{command_name}' executed successfully.")
            return 0
        except ValueError as ve:
            self.logger.error(f"Configuration error: {ve}")
            return 1
        except FileNotFoundError as fileNotFound:
            self.logger.error(f"File system error: {fileNotFound}")
            return 1
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during command '{args.command}': {e}", exc_info=True)
            return 1

# main.py
def main() -> int:
    args = parse_arguments()
    log_file_path = Path(args.log).resolve()
    logger = setup_logging(log_file=log_file_path, log_level_str=args.log_level)

    logger.info(f"Executing command: {args.command} with arguments: {vars(args)}")

    handler = CommandHandler(logger)
    return handler.execute(args)


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
