from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description="File Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Deduplicate command
    dedup_parser = subparsers.add_parser("deduplicate", help="Remove duplicate files")
    dedup_parser.add_argument("--path", required=True, help="Directory to deduplicate")
    dedup_parser.add_argument("--dry-run", action="store_true", help="Log duplicates without removing them")

    # Global arguments
    parser.add_argument("--src", help="Source directory path")
    parser.add_argument("--dst", help="Destination directory path")
    parser.add_argument("--log", help="Log file path")

    return parser.parse_args()