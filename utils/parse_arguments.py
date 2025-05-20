import argparse
from pathlib import Path


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="File management utility")

    # Main command argument
    parser.add_argument("--command", default="deduplicate",
                        help="Command to execute (deduplicate, move, etc.)")

    # Common arguments
    parser.add_argument("--log", default="app.log",
                        help="Log file path (default: app.log)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run without making changes")

    # Deduplicate command arguments
    parser.add_argument("--directory", type=Path,
                        help="Directory to process")
    parser.add_argument("--max-workers", type=int, default=4,
                        help="Maximum number of worker threads (default: 4)")

    # Move command arguments
    parser.add_argument("--src-dir", type=Path,
                        help="Source directory")
    parser.add_argument("--dst-dir", type=Path,
                        help="Destination directory")

    return parser.parse_args()
