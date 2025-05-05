import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def calculate_file_hash(file: Path, buffer_size: int = 65536) -> tuple:
    """
    Calculate the hash of a file using a buffered approach.

    Args:
        file (Path): The file to hash.
        buffer_size (int): Size of the buffer for reading the file.

    Returns:
        tuple: A tuple containing the file path and its hash.
    """
    hasher = hashlib.md5()
    with file.open("rb") as f:
        while chunk := f.read(buffer_size):
            hasher.update(chunk)
    return file, hasher.hexdigest()


def deduplicate(directory: str, dry_run: bool = False, max_workers: int = 4):
    """
    Identifies and removes duplicate files in the given directory using multi-threading.

    Args:
        directory (str): Path to the directory to deduplicate.
        dry_run (bool): If True, only logs duplicates without removing them.
        max_workers (int): Number of threads to use for hashing files.

    Returns:
        None
    """
    file_hashes = {}
    duplicates = []

    directory_path = Path(directory)
    if not directory_path.is_dir():
        raise ValueError(f"{directory} is not a valid directory.")

    files = (file for file in directory_path.rglob("*") if file.is_file())

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file, file_hash in executor.map(calculate_file_hash, files):
            if file_hash in file_hashes:
                duplicates.append(file)
            else:
                file_hashes[file_hash] = file

    if dry_run:
        print("Duplicates found:")
        for duplicate in duplicates:
            print(duplicate)
    else:
        for duplicate in duplicates:
            print(f"Removing duplicate: {duplicate}")
            duplicate.unlink()