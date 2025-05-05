# create a function that takes a directory path and returns a list of all files in that directory and its subdirectories

from pathlib import Path


def find_all_files_recursive(directory: Path) -> list[Path]:
    """
    Takes a directory path and returns a list of all files in that directory and its subdirectories.

    Args:
        directory (Path): The root directory to search.

    Returns:
        list[Path]: A list of file paths.
    """
    return [file for file in directory.rglob("*") if file.is_file()]
