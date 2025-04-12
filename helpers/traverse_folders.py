import shutil
from pathlib import Path


def traverse_folders(path=Path.cwd()):
    """
    Recursively loop through all folders and subfolders starting from the given path.
    Default path is the current working directory.
    """

    # Iterate through all items in the current path
    for item in path.iterdir():
        # Check if the item is a directory
        if item.is_dir():
            print(f"Found folder: {item}")

            try:
                # Attempt to delete the folder
                shutil.rmtree(item)
                print(f"Deleted folder: {item}")
            except OSError as e:
                print(f"Failed to delete folder {item}: {e}")
                # Recursively traverse the subdirectory
                traverse_folders(item)