import logging
from argparse import Namespace
from pathlib import Path
from typing import Dict, Type, Final, NoReturn

from Interface import CommandInterface
from functions import CommandType, DeleteHiddenFilesCommand, DeleteByExtensionCommand, MoveCommand, \
    CleanFolderCommand, DeleteEmptyFoldersCommand, CompressFilesCommand
from functions.FileDeduplicator import DeduplicateCommand
from functions.exceptions import *


class CommandRegistry:
    """Registry for available commands"""

    COMMAND_MAP: Final[Dict[str, Type[CommandInterface]]] = {
        CommandType.CommandType.DEDUPLICATE.name.lower(): DeduplicateCommand,
        CommandType.CommandType.MOVE.name.lower(): MoveCommand,
        CommandType.CommandType.DELETE_BY_EXTENSION.name.lower(): DeleteByExtensionCommand,
        CommandType.CommandType.CLEAN_FOLDER.name.lower(): CleanFolderCommand,
        CommandType.CommandType.DELETE_EMPTY.name.lower(): DeleteEmptyFoldersCommand,
        CommandType.CommandType.DELETE_HIDDEN_FILES.name.lower(): DeleteHiddenFilesCommand,
        CommandType.CommandType.COMPRESS_FILES.name.lower(): CompressFilesCommand,
    }

    def get_command(self, command_name: str) -> CommandInterface:
        command_class = self.COMMAND_MAP.get(command_name.lower())
        if not command_class:
            self._raise_unsupported_command_error(command_name)
        return command_class()

    def _raise_unsupported_command_error(self, command_name: str) -> NoReturn:
        valid_commands = ", ".join(self.COMMAND_MAP.keys())
        raise UnsupportedCommandError(
            f"Unsupported command: {command_name}. Supported commands are: {valid_commands}"
        )


class CommandHandler:
    """Handles execution of commands"""

    ERROR_MESSAGES: Final[Dict[Type[Exception], str]] = {
        ArgumentError: "Argument error",
        ValidationError: "Validation error",
        UnsupportedCommandError: "Command error",
        DirectoryError: "Directory error",
        FileError: "File error",
        PathError: "Path error",
        FileSystemError: "File system error",
        OperationError: "Operation error",
        CommandError: "Command error",
        FileManagerError: "File manager error",
    }

    def __init__(self, logger: logging.Logger) -> None:
        self._logger: logging.Logger = logger
        self._registry: CommandRegistry = CommandRegistry()

    def execute(self, args: Namespace) -> int:
        command_name = args.command.lower()
        try:
            return self._process_command(command_name, args)
        except Exception as error:
            return self._handle_error(error, command_name)

    def _process_command(self, command_name: str, args: Namespace) -> int:
        command = self._registry.get_command(command_name)
        command.validate(args)
        command.execute(args, self._logger)
        self._log_success(command_name)
        return 0

    def _handle_error(self, error: Exception, command_name: str) -> int:
        error_type = type(error)
        if error_type in self.ERROR_MESSAGES:
            self._log_known_error(error, error_type)
        else:
            self._log_unexpected_error(error, command_name)
        return 1

    def _log_success(self, command_name: str) -> None:
        self._logger.info(f"Command '{command_name}' executed successfully.")

    def _log_known_error(self, error: Exception, error_type: Type[Exception]) -> None:
        self._logger.error(f"{self.ERROR_MESSAGES[error_type]}: {error}")

    def _log_unexpected_error(self, error: Exception, command_name: str) -> None:
        self._logger.error(
            f"An unexpected error occurred during command '{command_name}': {error}",
            exc_info=True
        )


def main() -> int:
    from utils.parse_arguments import parse_arguments
    args = parse_arguments()
    log_file_path = Path(args.log).resolve()
    from utils.setup_logging import setup_logging
    logger = setup_logging(log_file=log_file_path, log_level_str=args.log_level)
    logger.info(f"Executing command: {args.command} with arguments: {vars(args)}")
    return CommandHandler(logger).execute(args)


if __name__ == "__main__":
    exit(main())