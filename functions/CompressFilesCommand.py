import logging
from argparse import Namespace
from pathlib import Path

from Interface.CommandInterface import CommandInterface


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
