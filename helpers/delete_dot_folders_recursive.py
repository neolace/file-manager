import shutil
from pathlib import Path


def delete_dot_folders_recursive(root_path: Path, dry_run: bool = False) -> None:
    """
    Find and remove all folders that start with '.' recursively.

    Args:
        root_path: The root directory to search in
        dry_run: If True, only show what would be deleted without actually deleting
    """
    root = Path(root_path)
    count = 0

    # Find all directories including hidden ones
    for folder in root.glob("**/*"):
        if folder.is_dir() and folder.name.startswith("."):
            count += 1
            if dry_run:
                print(f"Would delete: {folder}")
            else:
                try:
                    shutil.rmtree(folder)
                    print(f"Deleted folder: {folder}")
                except OSError as e:
                    print(f"Error deleting {folder}: {e}")

    print(f"Processed {count} folders starting with '.' under {root}")
