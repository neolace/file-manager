"""File Manager package: utilities for file and directory management."""

import sys

from main import main
from parse_arguments import parse_arguments

if __name__ == "__main__":
    args = parse_arguments()
    exit_code = main(
        dry_run=args.dry_run, src_path=args.src, dst_path=args.dst, log_path=args.log
    )
    sys.exit(exit_code)
