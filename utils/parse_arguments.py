from argparse import ArgumentParser, Namespace

# Constants for commands and arguments
COMMAND_DEDUPLICATE = "deduplicate"
ARG_LOG = "--log"
ARG_DRY_RUN = "--dry-run"
ARG_PATH = "--path"

def add_common_arguments(parser: ArgumentParser) -> None:
    """Add arguments that are common to all commands."""
    parser.add_argument(
        ARG_LOG.lstrip("-"),
        help="Path to the log file."
    )
    parser.add_argument(
        ARG_DRY_RUN.lstrip("-"),
        action="store_true",
        help="Simulate the command without making changes."
    )

def setup_deduplicate_command(subparsers) -> None:
    """Setup the deduplicate command and its specific arguments."""
    dedup_parser = subparsers.add_parser(
        COMMAND_DEDUPLICATE,
        help="Remove duplicate files in a directory."
    )
    dedup_parser.add_argument(
        ARG_PATH.lstrip("-"),
        required=True,
        help="Path to the directory to deduplicate."
    )

def parse_arguments() -> Namespace:
    """
    Parse command-line arguments for the File Manager CLI.

    This function sets up and parses command-line arguments for a file management tool.
    It supports multiple commands and options, including deduplication, logging, and dry-run mode.

    Returns:
        Namespace: Parsed arguments as a namespace object.
    """
    parser = ArgumentParser(description="File Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Setup arguments
    add_common_arguments(parser)
    setup_deduplicate_command(subparsers)

    return parser.parse_args()