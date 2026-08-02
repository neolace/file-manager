import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="File Management Utility")

    # Common arguments
    parser.add_argument(
        "--log", type=str, default="app.log", help="Path to the log file"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate actions without making changes"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (e.g., DEBUG, INFO, WARNING)",
    )

    # Command argument
    parser.add_argument(
        "--command",
        type=str,
        required=True,
        help="Command to execute (e.g., deduplicate, compress_files)",
    )

    # Deduplicate command arguments
    parser.add_argument(
        "--directory", type=str, help="Target directory for deduplication"
    )
    parser.add_argument(
        "--max-workers", type=int, default=1, help="Maximum number of worker threads"
    )

    # Delete by extension command arguments
    parser.add_argument("--path", type=str, help="Target directory for file operations")
    parser.add_argument(
        "--extensions",
        type=str,
        help="Comma-separated list of file extensions to delete",
    )

    # Clean folder command arguments
    parser.add_argument(
        "--excluded-names",
        type=str,
        help="Comma-separated list of names to exclude from cleaning",
    )

    # Delete empty folders command arguments
    parser.add_argument(
        "--recursive", action="store_true", help="Recursively delete empty folders"
    )

    return parser.parse_args()
