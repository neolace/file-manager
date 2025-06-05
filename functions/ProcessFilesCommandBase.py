import logging
from abc import abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import Optional, List, Callable

from Interface.CommandInterface import CommandInterface
from functions.exceptions import OperationError
from utils.file_filter import FileFilter
from utils.validate_arguments import validate_required_arg, validate_path, validate_extensions


def _parse_string_list_arg(arg_value: Optional[str | List[str]]) -> Optional[List[str]]:
    if isinstance(arg_value, str):
        return [item.strip() for item in arg_value.split(',') if item.strip()]
    return arg_value


class ProcessFilesCommandBase(CommandInterface):
    """Base class for commands that process files in a directory."""

    def validate(self, args: Namespace) -> None:
        # Validate required path argument
        path = validate_required_arg(args, 'path', self.description)

        # Validate that the path exists and is a directory
        validate_path(path, must_exist=True, must_be_dir=True)

        # Validate extensions if provided
        if hasattr(args, 'extensions') and args.extensions:
            validate_extensions(args.extensions)

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        extensions = _parse_string_list_arg(getattr(args, 'extensions', None))
        excluded_names = _parse_string_list_arg(getattr(args, 'excluded_names', None))

        file_operation = self._get_file_operation(args, logger)

        if not file_operation:
            raise OperationError(f"No file operation defined for the '{self.description}' command.")

        # Process the files in the specified path
        path_obj = Path(args.path)
        count = 0

        for file_path in self._get_files_to_process(path_obj, extensions, excluded_names):
            try:
                file_operation(str(file_path))
                count += 1
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                # Re-raise as OperationError to provide more context
                raise OperationError(f"Failed to process file {file_path}: {e}") from e

        logger.info(f"Processed {count} files.")
        logger.info(f"'{self.description}' command finished processing path '{args.path}'.")

    # noinspection PyMethodMayBeStatic
    def _get_files_to_process(self, directory: Path, extensions: Optional[List[str]] = None,
                              excluded_names: Optional[List[str]] = None) -> List[Path]:
        """Return a list of files to the process based on given filters."""
        file_filter = FileFilter(extensions=extensions, excluded_names=excluded_names)
        return file_filter.filter_files(directory)

    @abstractmethod
    def _get_file_operation(self, args: Namespace, logger: logging.Logger) -> Callable[[str], None]:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
