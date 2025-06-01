import logging
from argparse import Namespace
from pathlib import Path

from Interface.CommandInterface import CommandInterface


class MoveCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Move files between directories"

    def validate(self, args: Namespace) -> None:
        if not args.src_dir or not args.dst_dir:
            raise ValueError("Both 'src_dir' and 'dst_dir' arguments are required for the 'move' command.")
        if not Path(args.src_dir).is_dir():
            raise ValueError(f"Source directory not found: {args.src_dir}")
        try:
            Path(args.dst_dir)
        except Exception:
            raise ValueError(f"Invalid destination directory path: {args.dst_dir}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        logger.info(
            f"Move operation called for src: {args.src_dir}, dst: {args.dst_dir}. Dry run: {args.dry_run}"
        )
        logger.warning("MoveCommand execute method is not yet implemented.")
