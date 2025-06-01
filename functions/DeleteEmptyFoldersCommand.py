import logging
import os
from argparse import Namespace
from pathlib import Path

from Interface.CommandInterface import CommandInterface


class DeleteEmptyFoldersCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Delete empty folders, optionally recursively"

    def validate(self, args: Namespace) -> None:
        if not args.path:
            raise ValueError(f"'path' argument is required for the '{self.description}' command.")
        path_obj = Path(args.path)
        if not path_obj.exists():
            raise ValueError(f"Path not found: {args.path}")
        if not path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {args.path}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        target_path = Path(args.path)
        recursive = getattr(args, 'recursive', True)
        deleted_count = 0

        for root, dirs, files in os.walk(target_path, topdown=False):
            if not recursive and Path(root) != target_path:
                continue

            if not os.listdir(root):
                try:
                    if not args.dry_run:
                        os.rmdir(root)
                        logger.info(f"Deleted empty folder: {root}")
                    else:
                        logger.info(f"[DRY RUN] Would delete empty folder: {root}")
                    deleted_count += 1
                except OSError as e:
                    logger.error(f"Failed to delete empty folder {root}: {e}")

            if not recursive:
                break

        action = "Would delete" if args.dry_run else "Deleted"
        logger.info(f"{action} {deleted_count} empty folder(s) under '{target_path}'.")
