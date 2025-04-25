import argparse


def parse_arguments():
    """
    Parse command line arguments for the file manager application.

    Returns:
        argparse.Namespace: The parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="File Management Utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Move command
    move_parser = subparsers.add_parser("move", help="Move files from source to target")
    move_parser.add_argument("--source", required=True, help="Source directory")
    move_parser.add_argument("--target", required=True, help="Target directory")
    move_parser.add_argument("--type", required=True, help="File type to move")
    move_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )
    move_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed output"
    )

    # Delete command
    delete_parser = subparsers.add_parser(
        "delete", help="Delete files matching criteria"
    )
    delete_parser.add_argument("--path", required=True, help="Directory to search in")
    delete_parser.add_argument("--type", required=True, help="File type to delete")
    delete_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )
    delete_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed output"
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove files by name pattern")
    remove_parser.add_argument("--path", required=True, help="Directory to search in")
    remove_parser.add_argument("--name", required=True, help="Name pattern to match")
    remove_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )
    remove_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed output"
    )

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean directory of temp files")
    clean_parser.add_argument("--path", required=True, help="Directory to clean")
    clean_parser.add_argument(
        "--all", action="store_true", help="Remove all temporary files"
    )
    clean_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed output"
    )

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract archive files")
    extract_parser.add_argument("--path", required=True, help="Directory with archives")
    extract_parser.add_argument("--7zip", dest="_7zip", help="Path to 7zip executable")

    # Copy command
    copy_parser = subparsers.add_parser("copy", help="Copy files from source to target")
    copy_parser.add_argument("--source", required=True, help="Source directory")
    copy_parser.add_argument("--target", required=True, help="Target directory")
    copy_parser.add_argument("--type", required=True, help="File type to copy")
    copy_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )
    copy_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed output"
    )

    # Find duplicates command
    dupes_parser = subparsers.add_parser("find-dupes", help="Find duplicate files")
    dupes_parser.add_argument(
        "--path", required=True, help="Directory to search for duplicates"
    )

    # Organize by date command
    date_parser = subparsers.add_parser("organize-date", help="Organize files by date")
    date_parser.add_argument("--source", required=True, help="Source directory")
    date_parser.add_argument("--target", required=True, help="Target directory")
    date_parser.add_argument(
        "--format", default="%Y/%m/%d", help="Directory format (default: %%Y/%%m/%%d)"
    )
    date_parser.add_argument(
        "--use-created",
        action="store_true",
        help="Use created date instead of modified",
    )

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for text in files")
    search_parser.add_argument("--path", required=True, help="Directory to search in")
    search_parser.add_argument("--text", required=True, help="Text to search for")
    search_parser.add_argument(
        "--extensions", nargs="+", help="File extensions to search in"
    )
    search_parser.add_argument(
        "--case-sensitive", action="store_true", help="Use case-sensitive search"
    )

    # Process extensions command
    process_parser = subparsers.add_parser(
        "process-extensions", help="Process files by extension"
    )
    process_parser.add_argument("--path", required=True, help="Directory to process")
    process_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)
