import logging
from abc import abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import Optional, List, Callable

from Interface.CommandInterface import CommandInterface
from utils.fm_process_files import process_files  # Assuming this will be updated


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
