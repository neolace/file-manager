import logging
from argparse import Namespace

from Interface.CommandInterface import CommandInterface
from utils.validate_arguments import validate_required_arg, validate_path


class MoveCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Move files between directories"

    def validate(self, args: Namespace) -> None:
        # Validate required source directory argument
        src_dir = validate_required_arg(args, 'src_dir', self.description)

        # Validate required destination directory argument
        dst_dir = validate_required_arg(args, 'dst_dir', self.description)

        # Validate that the source directory exists and is a directory
        validate_path(src_dir, must_exist=True, must_be_dir=True)

        # Validate that the destination directory path is valid
        # We don't require it to exist, as we might create it during execution
        validate_path(dst_dir, must_exist=False)

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        logger.info(
            f"Move operation called for src: {args.src_dir}, dst: {args.dst_dir}. Dry run: {args.dry_run}"
        )
        logger.warning("MoveCommand execute method is not yet implemented.")
