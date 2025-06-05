import logging
import os
import stat  # Required for DeleteHiddenFilesCommand
from argparse import Namespace
from pathlib import Path
from typing import Callable

from functions.ProcessFilesCommandBase import ProcessFilesCommandBase


class DeleteHiddenFilesCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Delete hidden files, optionally excluding some names"

    def _get_file_operation(self, args: Namespace, logger: logging.Logger) -> Callable[[str], None]:
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
                    if not args.dry_run:
                        os.remove(file_path_str)
                        logger.info(f"Deleted hidden file: {file_path_str}")
                    else:
                        logger.info(f"[DRY RUN] Would delete hidden file: {file_path_str}")
            except OSError as e:
                logger.error(f"Error during hidden file check/delete for {file_path_str}: {e}")

        return operation_func
