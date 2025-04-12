import argparse


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="File Manager - Organize and manage files"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Move files command
    move_parser = subparsers.add_parser("move", help="Move files of a specific type")
    move_parser.add_argument(
        "--source", "-s", type=str, required=True, help="Source folder path"
    )
    move_parser.add_argument(
        "--target", "-t", type=str, required=True, help="Target folder path"
    )
    move_parser.add_argument(
        "--type", type=str, required=True, help="File extension to move"
    )
    move_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Delete files command
    delete_parser = subparsers.add_parser("delete", help="Delete files by extension")
    delete_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to search in"
    )
    delete_parser.add_argument(
        "--type", type=str, required=True, help="File extension to delete"
    )
    delete_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Remove folder command
    remove_parser = subparsers.add_parser("remove", help="Remove folders by name")
    remove_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to search in"
    )
    remove_parser.add_argument(
        "--name", "-n", type=str, required=True, help="Folder name to remove"
    )
    remove_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Clean folders command
    clean_parser = subparsers.add_parser("clean", help="Clean empty folders")
    clean_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to clean"
    )
    clean_parser.add_argument(
        "--all", action="store_true", help="Remove all folders, not just empty ones"
    )

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract 7z archives")
    extract_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Folder with 7z archives"
    )
    extract_parser.add_argument(
        "--7zip",
        type=str,
        default="C:/Program Files/7-Zip/7z.exe",
        help="Path to 7zip executable",
    )

    # Copy files command
    copy_parser = subparsers.add_parser("copy", help="Copy files of a specific type")
    copy_parser.add_argument(
        "--source", "-s", type=str, required=True, help="Source folder path"
    )
    copy_parser.add_argument(
        "--target", "-t", type=str, required=True, help="Target folder path"
    )
    copy_parser.add_argument(
        "--type", type=str, required=True, help="File extension to copy"
    )
    copy_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Rename files command
    rename_parser = subparsers.add_parser("rename", help="Rename files by extension")
    rename_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to search in"
    )
    rename_parser.add_argument(
        "--type", type=str, required=True, help="File extension to rename"
    )
    rename_parser.add_argument(
        "--name", "-n", type=str, required=True, help="New base name for files"
    )
    rename_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Find duplicates command
    dupe_parser = subparsers.add_parser("find-dupes", help="Find duplicate files")
    dupe_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to search in"
    )

    # Organize by date command
    organize_parser = subparsers.add_parser(
        "organize-date", help="Organize files by date"
    )
    organize_parser.add_argument(
        "--source", "-s", type=str, required=True, help="Source folder path"
    )
    organize_parser.add_argument(
        "--target", "-t", type=str, required=True, help="Target folder path"
    )
    organize_parser.add_argument(
        "--format",
        type=str,
        default="%Y-%m",
        help="Date format for folders (default: YYYY-MM)",
    )
    organize_parser.add_argument(
        "--use-created",
        action="store_true",
        help="Use creation date instead of modified date",
    )
    organize_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Search by content command
    search_parser = subparsers.add_parser("search", help="Search files by content")
    search_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to search in"
    )
    search_parser.add_argument(
        "--text", "-t", type=str, required=True, help="Text to search for"
    )
    search_parser.add_argument(
        "--extensions", "-e", type=str, nargs="+", help="File extensions to search in"
    )
    search_parser.add_argument(
        "--case-sensitive", action="store_true", help="Make search case-sensitive"
    )

    # Process extensions command
    process_ext_parser = subparsers.add_parser(
        "process-extensions", help="Process files with multiple extensions"
    )
    process_ext_parser.add_argument(
        "--path", "-p", type=str, required=True, help="Root path to process"
    )
    process_ext_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )

    # Verbosity
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()