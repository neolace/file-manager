import logging
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, Final, NoReturn, Type

from functions.CleanFolderCommand import CleanFolderCommand
from functions.CompressFilesCommand import CompressFilesCommand
from functions.DeleteByExtensionCommand import DeleteByExtensionCommand
from functions.DeleteEmptyFoldersCommand import DeleteEmptyFoldersCommand
from functions.DeleteHiddenFilesCommand import DeleteHiddenFilesCommand
from functions.exceptions import (
    ArgumentError,
    CommandError,
    DirectoryError,
    FileError,
    FileManagerError,
    FileSystemError,
    OperationError,
    PathError,
    UnsupportedCommandError,
    ValidationError,
)
from functions.FileDeduplicator import DeduplicateCommand
from Interface.CommandInterface import CommandInterface, CommandResult
from Interface.FileSystemExecutor import (
    FileSystemExecutor,
    RealFileSystemExecutor,
    RecordingFileSystemExecutor,
)


class CommandRegistry:
    """Registry for available commands"""

    COMMAND_MAP: Final[Dict[str, Type[CommandInterface[Any, Any]]]] = {
        "deduplicate": DeduplicateCommand,
        "delete_by_extension": DeleteByExtensionCommand,
        "clean_folder": CleanFolderCommand,
        "delete_empty": DeleteEmptyFoldersCommand,
        "delete_hidden_files": DeleteHiddenFilesCommand,
        "compress_files": CompressFilesCommand,
    }

    def get_command(self, command_name: str) -> CommandInterface[Any, Any]:
        command_class = self.COMMAND_MAP.get(command_name.lower())
        if not command_class:
            self._raise_unsupported_command_error(command_name)
        return command_class()

    def _raise_unsupported_command_error(self, command_name: str) -> NoReturn:
        valid_commands = ", ".join(self.COMMAND_MAP.keys())
        raise UnsupportedCommandError(
            f"Unsupported command: {command_name}. "
            f"Supported commands are: {valid_commands}"
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
        try:
            command_name = args.command.lower()
            return self._process_command(command_name, args)
        except Exception as error:
            command_name = getattr(args, "command", "unknown")
            return self._handle_error(error, command_name)

    def _process_command(self, command_name: str, args: Namespace) -> int:
        command = self._registry.get_command(command_name)
        executor = self._select_executor(bool(getattr(args, "dry_run", False)))
        request = command.parse(args, executor)
        result = command.execute(request, self._logger)
        if not result.ok:
            for error in result.errors:
                self._logger.error("Operation failed: %s", error)
            return 1
        self._log_success(command_name, result)
        return 0

    @staticmethod
    def _select_executor(dry_run: bool) -> FileSystemExecutor:
        if dry_run:
            return RecordingFileSystemExecutor()
        return RealFileSystemExecutor()

    def _handle_error(self, error: Exception, command_name: str) -> int:
        for error_type, message in self.ERROR_MESSAGES.items():
            if isinstance(error, error_type):
                self._logger.error("%s: %s", message, error)
                break
        else:
            self._log_unexpected_error(error, command_name)
        return 1

    def _log_success(self, command_name: str, result: CommandResult) -> None:
        self._logger.info(
            "Command '%s' executed successfully: %d succeeded, %d skipped.",
            command_name,
            result.succeeded,
            result.skipped,
        )

    def _log_unexpected_error(self, error: Exception, command_name: str) -> None:
        self._logger.error(
            f"An unexpected error occurred during command '{command_name}': {error}",
            exc_info=True,
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
