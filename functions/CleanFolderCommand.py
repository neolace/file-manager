import logging
import os
from argparse import Namespace
from typing import Callable

from functions.ProcessFilesCommandBase import ProcessFilesCommandBase


class CleanFolderCommand(ProcessFilesCommandBase):
    def description(self) -> str:
        return "Clean a folder by deleting its contents (files), optionally excluding some names"

    def _get_file_operation(cmd_args: Namespace, cmd_logger: logging.Logger) -> Callable[[str], None]:
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
