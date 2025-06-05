import logging
import os
from argparse import Namespace
from typing import Callable

from functions.ProcessFilesCommandBase import ProcessFilesCommandBase
from functions.exceptions import OperationError
from utils.validate_arguments import validate_required_arg, validate_extensions


class DeleteByExtensionCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Delete files by specified extensions in a directory"

    def validate(self, args: Namespace) -> None:
        super().validate(args)

        # Validate that extensions are provided
        extensions = validate_required_arg(args, 'extensions', self.description)

        # Validate the extensions format
        validate_extensions(extensions)

    def _get_file_operation(self, args: Namespace, logger: logging.Logger) -> Callable[[str], None]:
        def operation_func(file_path_str: str):
            if not args.dry_run:
                try:
                    os.remove(file_path_str)
                    logger.info(f"Deleted by extension: {file_path_str}")
                except OSError as e:
                    logger.error(f"Failed to delete by extension {file_path_str}: {e}")
                    raise OperationError(f"Failed to delete file {file_path_str}: {e}") from e
            else:
                logger.info(f"[DRY RUN] Would delete by extension: {file_path_str}")

        return operation_func
