from argparse import ArgumentParser

def parse_arguments():
    """
    Parse command-line arguments for the File Manager CLI.

    This function sets up and parses command-line arguments for a file management tool.
    It supports multiple commands and options, including deduplication, logging, and dry-run mode.

    Commands:
        - deduplicate: Remove duplicate files in a specified directory.

    Options:
        --log: Specify the path to the log file.
        --dry-run: Run the command without making any changes (simulation mode).

    Returns:
        argparse.Namespace: Parsed arguments as a namespace object.
    """
    parser = ArgumentParser(description="File Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add common arguments
    parser.add_argument("--log", help="Path to the log file.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the command without making changes.")

    # Add specific commands
    dedup_parser = subparsers.add_parser("deduplicate", help="Remove duplicate files in a directory.")
    dedup_parser.add_argument("--path", required=True, help="Path to the directory to deduplicate.")

    return parser.parse_args()