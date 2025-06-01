import logging
import os
import stat  # Required for DeleteHiddenFilesCommand
from abc import ABC, abstractmethod
from argparse import Namespace
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Type, Optional, List, Callable

from functions.FileDeduplicator import FileDeduplicator
from utils.fm_process_files import process_files  # Assuming this will be updated
from utils.parse_arguments import parse_arguments
from utils.setup_logging import setup_logging


class CommandType(Enum):
    """Supported command types"""
    DEDUPLICATE = auto()
    MOVE = auto()
    DELETE_BY_EXTENSION = auto()
    CLEAN_FOLDER = auto()
    DELETE_EMPTY = auto()
    DELETE_HIDDEN_FILES = auto()  # Renamed from DELETE_HIDDEN


class CommandInterface(ABC):
    """Base interface for all commands"""

    @abstractmethod
    def validate(self, args: Namespace) -> None:
        pass

    @abstractmethod
    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


class DeduplicateCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Deduplicate files in a directory"

    def validate(self, args: Namespace) -> None:
        if not args.directory:
            raise ValueError("'directory' argument is required for the 'deduplicate' command.")
        if not Path(args.directory).is_dir():
            raise ValueError(f"Directory not found: {args.directory}")

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
            raise ValueError("Both 'src_dir' and 'dst_dir' arguments are required for the 'move' command.")
        if not Path(args.src_dir).is_dir():
            raise ValueError(f"Source directory not found: {args.src_dir}")
        try:
            Path(args.dst_dir)
        except Exception:
            raise ValueError(f"Invalid destination directory path: {args.dst_dir}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        logger.info(
            f"Move operation called for src: {args.src_dir}, dst: {args.dst_dir}. Dry run: {args.dry_run}"
        )
        logger.warning("MoveCommand execute method is not yet implemented.")


class ProcessFilesCommandBase(CommandInterface):
    """Base class for commands using the fm_process_files.py function."""

    def validate(self, args: Namespace) -> None:
        if not args.path:
            raise ValueError(f"'path' argument is required for the '{self.description}' command.")
        path_obj = Path(args.path)
        if not path_obj.exists():
            raise ValueError(f"Path not found: {args.path}")
        if not path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {args.path}")

    def _parse_string_list_arg(self, arg_value: Optional[str | List[str]]) -> Optional[List[str]]:
        if isinstance(arg_value, str):
            return [item.strip() for item in arg_value.split(',') if item.strip()]
        return arg_value

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        extensions = self._parse_string_list_arg(getattr(args, 'extensions', None))
        excluded_names = self._parse_string_list_arg(getattr(args, 'excluded_names', None))

        file_operation = self._get_file_operation(args, logger)

        process_files(
            operation=file_operation,
            path=Path(args.path),
            extensions=extensions,
            excluded_names=excluded_names,
            dry_run=args.dry_run,
            recursive=getattr(args, 'recursive', True),
            log_file=Path(args.log)
        )
        logger.info(f"'{self.description}' command finished processing path '{args.path}'.")

    @abstractmethod
    def _get_file_operation(self, args: Namespace, logger: logging.Logger) -> Callable[[str], None]:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


class DeleteByExtensionCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Delete files by specified extensions in a directory"

    def validate(self, args: Namespace) -> None:
        super().validate(args)
        if not getattr(args, 'extensions', None):
            raise ValueError(f"'extensions' parameter is required for the '{self.description}' command.")

    def _get_file_operation(self, cmd_args: Namespace, cmd_logger: logging.Logger) -> Callable[[str], None]:
        def operation_func(file_path_str: str):
            if not cmd_args.dry_run:
                try:
                    os.remove(file_path_str)
                    cmd_logger.info(f"Deleted by extension: {file_path_str}")
                except OSError as e:
                    cmd_logger.error(f"Failed to delete by extension {file_path_str}: {e}")
            else:
                cmd_logger.info(f"[DRY RUN] Would delete by extension: {file_path_str}")

        return operation_func


class CleanFolderCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Clean a folder by deleting its contents (files), optionally excluding some names"

    def _get_file_operation(self, cmd_args: Namespace, cmd_logger: logging.Logger) -> Callable[[str], None]:
        def operation_func(file_path_str: str):
            if not cmd_args.dry_run:
                try:
                    os.remove(file_path_str)
                    cmd_logger.info(f"CleanFolder: Deleted {file_path_str}")
                except OSError as e:
                    cmd_logger.error(f"CleanFolder: Failed to delete {file_path_str}: {e}")
            else:
                cmd_logger.info(f"[DRY RUN] CleanFolder: Would delete {file_path_str}")

        return operation_func


class DeleteHiddenFilesCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Delete hidden files, optionally excluding some names"

    def _get_file_operation(self, cmd_args: Namespace, cmd_logger: logging.Logger) -> Callable[[str], None]:
        def operation_func(file_path_str: str):
            try:
                is_hidden = False
                p_obj = Path(file_path_str)
                if os.name == 'nt':
                    attrs = os.stat(file_path_str).st_file_attributes
                    if attrs & stat.FILE_ATTRIBUTE_HIDDEN:
                        is_hidden = True
                elif p_obj.name.startswith('.'):
                    is_hidden = True

                if is_hidden:
                    if not cmd_args.dry_run:
                        os.remove(file_path_str)
                        cmd_logger.info(f"Deleted hidden file: {file_path_str}")
                    else:
                        cmd_logger.info(f"[DRY RUN] Would delete hidden file: {file_path_str}")
            except OSError as e:
                cmd_logger.error(f"Error during hidden file check/delete for {file_path_str}: {e}")

        return operation_func


class DeleteEmptyFoldersCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Delete empty folders, optionally recursively"

    def validate(self, args: Namespace) -> None:
        if not args.path:
            raise ValueError(f"'path' argument is required for the '{self.description}' command.")
        path_obj = Path(args.path)
        if not path_obj.exists():
            raise ValueError(f"Path not found: {args.path}")
        if not path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {args.path}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        target_path = Path(args.path)
        recursive = getattr(args, 'recursive', True)
        deleted_count = 0

        for root, dirs, files in os.walk(target_path, topdown=False):
            if not recursive and Path(root) != target_path:
                continue

            if not os.listdir(root):
                try:
                    if not args.dry_run:
                        os.rmdir(root)
                        logger.info(f"Deleted empty folder: {root}")
                    else:
                        logger.info(f"[DRY RUN] Would delete empty folder: {root}")
                    deleted_count += 1
                except OSError as e:
                    logger.error(f"Failed to delete empty folder {root}: {e}")

            if not recursive:
                break

        action = "Would delete" if args.dry_run else "Deleted"
        logger.info(f"{action} {deleted_count} empty folder(s) under '{target_path}'.")


class RenameFilesCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Rename files in a directory based on specified criteria"

    def validate(self, args: Namespace) -> None:
        if not args.path:
            raise ValueError("'path' argument is required for the 'rename_files' command.")
        path_obj = Path(args.path)
        if not path_obj.exists():
            raise ValueError(f"Path not found: {args.path}")
        if not path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {args.path}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        logger.info(f"Renaming files in directory: {args.path}. Dry run: {args.dry_run}")
        logger.warning("RenameFilesCommand execute method is not yet implemented.")


class CompressFilesCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Compress files in a directory into a single archive"

    def validate(self, args: Namespace) -> None:
        if not args.path:
            raise ValueError("'path' argument is required for the 'compress_files' command.")
        path_obj = Path(args.path)
        if not path_obj.exists():
            raise ValueError(f"Path not found: {args.path}")
        if not path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {args.path}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        logger.info(f"Compressing files in directory: {args.path}. Dry run: {args.dry_run}")
        logger.warning("CompressFilesCommand execute method is not yet implemented.")


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
            self.logger.info(f"Command '{command_name}' ({command.description}) executed successfully.")
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
