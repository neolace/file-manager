import logging
import os
import zipfile
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from Interface.CommandInterface import CommandInterface
from functions.exceptions import OperationError
from utils.file_filter import FileFilter
from utils.validate_arguments import validate_required_arg, validate_path, validate_extensions


def _parse_string_list_arg(arg_value: Optional[str]) -> Optional[List[str]]:
    if isinstance(arg_value, str):
        return [item.strip() for item in arg_value.split(',') if item.strip()]
    return None


class CompressFilesCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Compress files in a directory into a single archive"

    def validate(self, args: Namespace) -> None:
        # Validate required path argument
        path = validate_required_arg(args, 'path', self.description)

        # Validate that the path exists and is a directory
        validate_path(path, must_exist=True, must_be_dir=True)

        # Validate extensions if provided
        if hasattr(args, 'extensions') and args.extensions:
            validate_extensions(args.extensions)

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        logger.info(f"Compressing files in directory: {args.path}. Dry run: {args.dry_run}")

        path_obj = Path(args.path)
        extensions = _parse_string_list_arg(getattr(args, 'extensions', None))
        excluded_names = _parse_string_list_arg(getattr(args, 'excluded_names', None))

        # Generate archive name based on directory name and current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{path_obj.name}_{timestamp}.zip"
        archive_path = path_obj.parent / archive_name

        # Get list of files to compress using FileFilter
        file_filter = FileFilter(extensions=extensions, excluded_names=excluded_names)
        files_to_compress = file_filter.filter_files(path_obj)

        # Log skipped files if debug logging is enabled
        if logger.isEnabledFor(logging.DEBUG):
            for file_path in path_obj.rglob('*'):
                if file_path.is_file() and file_path not in files_to_compress:
                    if excluded_names and any(excluded in file_path.name for excluded in excluded_names):
                        logger.debug(f"Skipping excluded file: {file_path}")
                    elif extensions and file_path.suffix.lower().lstrip('.') not in [ext.lower().lstrip('.') for ext in extensions]:
                        logger.debug(f"Skipping file with non-matching extension: {file_path}")

        if not files_to_compress:
            logger.warning(f"No files found to compress in {args.path}")
            return

        logger.info(f"Found {len(files_to_compress)} files to compress")

        if args.dry_run:
            logger.info(f"[DRY RUN] Would create archive: {archive_path}")
            for file_path in files_to_compress:
                logger.info(f"[DRY RUN] Would add to archive: {file_path}")
        else:
            try:
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_path in files_to_compress:
                        # Store files with relative paths
                        arcname = file_path.relative_to(path_obj)
                        logger.debug(f"Adding to archive: {file_path} as {arcname}")
                        zip_file.write(file_path, arcname)

                logger.info(f"Successfully created archive: {archive_path}")
                logger.info(f"Archive size: {os.path.getsize(archive_path) / (1024*1024):.2f} MB")
            except Exception as e:
                logger.error(f"Failed to create archive: {e}")
                raise OperationError(f"Failed to create archive: {e}") from e
