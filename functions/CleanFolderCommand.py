import logging
import os
from argparse import Namespace
from typing import Callable

from functions.ProcessFilesCommandBase import ProcessFilesCommandBase


class CleanFolderCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Clean a folder by deleting its contents (files), optionally excluding some names"

    def _get_file_operation(self, args: Namespace, logger: logging.Logger) -> Callable[[str], None]:
        def operation_func(file_path_str: str):
            if not args.dry_run:
                try:
                    os.remove(file_path_str)
                    logger.info(f"CleanFolder: Deleted {file_path_str}")
                except OSError as e:
                    logger.error(f"CleanFolder: Failed to delete {file_path_str}: {e}")
            else:
                logger.info(f"[DRY RUN] CleanFolder: Would delete {file_path_str}")

        return operation_func
