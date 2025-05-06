import hashlib
from concurrent.futures import ThreadPoolExecutor
from logging import Logger
from pathlib import Path
from typing import Optional


def calculate_file_hash(file: Path,
                        buffer_size: int = 65536) -> tuple:
    """
    Calculate the hash of a file using a buffered approach.

    Args:
        file (Path): The file to hash.
        buffer_size (int): Size of the buffer for reading the file.

    Returns:
        tuple: A tuple containing the file path and its hash.
        :param file:
        :param buffer_size:
    """
    hasher = hashlib.md5()
    with file.open("rb") as f:
        while chunk := f.read(buffer_size):
            hasher.update(chunk)
    return file, hasher.hexdigest()


def deduplicate(directory: str,
                max_workers: int = 1,
                logger: Optional[Logger] = None,
                dry_run: bool = False):
    """
    Deduplicate files in a directory by removing duplicates based on their hash.

    Args:
        directory (str): The directory to search for duplicates.
        max_workers (int): Number of threads to use for hashing files.
        logger (Logger, optional): Logger instance for output.
        dry_run (bool): If True, only log actions without deleting anything.
    """

    if logger is None:
        import logging

        logger = logging.getLogger(__name__)

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

        for duplicate in duplicates:
            try:
                duplicate.unlink()
                logger.info(f"Removed duplicate: {duplicate}")
            except OSError as e:
                logger.error(f"Error removing {duplicate}: {e}")

        if dry_run:
            logger.info(f"Dry run: {len(duplicates)} duplicates found.")