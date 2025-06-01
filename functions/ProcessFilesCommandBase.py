import logging
from abc import abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import Optional, List, Callable

from Interface.CommandInterface import CommandInterface


def _parse_string_list_arg(arg_value: Optional[str | List[str]]) -> Optional[List[str]]:
    if isinstance(arg_value, str):
        return [item.strip() for item in arg_value.split(',') if item.strip()]
    return arg_value


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

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        extensions = _parse_string_list_arg(getattr(args, 'extensions', None))
        excluded_names = _parse_string_list_arg(getattr(args, 'excluded_names', None))

        file_operation = self._get_file_operation(args, logger)

        if not file_operation:
            raise ValueError(f"No file operation defined for the '{self.description}' command.")

        # Process the files in the specified path
        path_obj = Path(args.path)
        count = 0

        for file_path in self._get_files_to_process(path_obj, extensions, excluded_names):
            try:
                file_operation(str(file_path))
                count += 1
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")

        logger.info(f"Processed {count} files.")
        logger.info(f"'{self.description}' command finished processing path '{args.path}'.")

    # noinspection PyMethodMayBeStatic
    def _get_files_to_process(self, directory: Path, extensions: Optional[List[str]] = None,
                              excluded_names: Optional[List[str]] = None) -> List[Path]:
        """Return a list of files to the process based on given filters."""
        files = []

        for path in directory.rglob('*'):
            if not path.is_file():
                continue

            # Skip files with excluded names
            if excluded_names and any(excluded in path.name for excluded in excluded_names):
                continue

            # Filter by extensions if specified
            if extensions and path.suffix.lower().lstrip('.') not in [ext.lower().lstrip('.') for ext in extensions]:
                continue

            files.append(path)

        return files

    @abstractmethod
    def _get_file_operation(self, args: Namespace, logger: logging.Logger) -> Callable[[str], None]:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
