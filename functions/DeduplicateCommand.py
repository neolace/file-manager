import logging
from argparse import Namespace

from Interface.CommandInterface import CommandInterface


class DeduplicateCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Deduplicate files in a directory"

    def validate(self, args: Namespace) -> None:
        if not args.directory:
            raise ValueError("'directory' argument is required for the 'deduplicate' command.")
        from pathlib import Path
        if not Path(args.directory).is_dir():
            raise ValueError(f"Directory not found: {args.directory}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        from functions.FileDeduplicator import FileDeduplicator
        deduplicator = FileDeduplicator(
            directory=args.directory,
            max_workers=args.max_workers,
            logger=logger,
            dry_run=args.dry_run,
        )
        deduplicator.deduplicate()
