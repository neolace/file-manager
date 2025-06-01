import logging
import os
from argparse import Namespace
from typing import Callable

from functions.ProcessFilesCommandBase import ProcessFilesCommandBase


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
