import hashlib
from concurrent.futures import ThreadPoolExecutor
from logging import Logger
from pathlib import Path
from typing import Optional, Iterator, Dict, List, Tuple, Callable, Any, TypeVar

from config.settings import Config

# Type aliases
FileHashResult = Tuple[Path, str]
T = TypeVar('T')


def safe_action(func: Callable[..., T]) -> Callable[..., Optional[T]]:
    """
    A decorator that wraps a function to handle exceptions safely.
    
    Args:
        func: The function to wrap.
        
    Returns:
        A wrapped function that catches exceptions and returns None on failure.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {func.__name__}: {e}")
            return None

    return wrapper


class FileDeduplicator:
    def __init__(
            self,
            directory: str,
            logger: Logger,
            max_workers: int = Config.DEFAULT_MAX_WORKERS,
            dry_run: bool = False,
    ) -> None:
        self.directory_path = Path(directory)
        self.max_workers = max_workers
        self.logger = logger
        self.dry_run = dry_run
        self.file_hashes: Dict[str, Path] = {}
        self.duplicates: List[Path] = []

    @staticmethod
    def _calculate_file_hash(file: Path) -> FileHashResult:
        """Calculate the hash of a file using a buffered approach.

        Args:
            file: The file to hash.

        Returns:
            A tuple containing the file path and its MD5 hash.
        """
        hasher = hashlib.md5()
        try:
            with file.open("rb") as f:
                while chunk := f.read(Config.DEFAULT_BUFFER_SIZE):
                    hasher.update(chunk)
        except UnicodeEncodeError as e:
            print(f"File: {file.name} - Encoding error: {e}")
        return file, hasher.hexdigest()

    def _get_files(self) -> Iterator[Path]:
        """Get all files in the directory recursively."""
        if not self.directory_path.is_dir():
            raise ValueError(f"{self.directory_path} is not a valid directory.")
        return (file for file in self.directory_path.rglob("*") if file.is_file())

    def _find_duplicates(self) -> None:
        """Find duplicate files based on their hash."""
        self.file_hashes.clear()
        self.duplicates.clear()

        self.logger.info(f"Scanning for files in {self.directory_path}")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Process files in parallel
            for file, file_hash in executor.map(
                    self._calculate_file_hash, self._get_files()
            ):
                if file_hash in self.file_hashes:
                    self.duplicates.append(file)
                    self.logger.debug(f"Found duplicate: {file} (matches {self.file_hashes[file_hash]})")
                else:
                    self.file_hashes[file_hash] = file

        self.logger.info(
            f"Found {len(self.duplicates)} duplicates out of {len(self.file_hashes) + len(self.duplicates)} files")

    def _remove_duplicate(self, duplicate: Path) -> None:
        """Remove a duplicate file and log the action."""
        try:
            if not self.dry_run:
                duplicate.unlink()
            self.logger.info(
                f"{'Dry run: Would remove' if self.dry_run else 'Removed'} duplicate: {duplicate}"
            )
        except OSError as e:
            self.logger.error(f"Error removing {duplicate}: {e}")

    def _remove_duplicates(self) -> None:
        """Remove all identified duplicate files."""
        for duplicate in self.duplicates:
            self._remove_duplicate(duplicate)

    def get_statistics(self) -> Dict[str, int]:
        """Return statistics about the deduplication process.
        
        Returns:
            A dictionary with statistics like total files, unique files, and duplicates.
        """
        return {
            "total_files": len(self.file_hashes) + len(self.duplicates),
            "unique_files": len(self.file_hashes),
            "duplicates": len(self.duplicates)
        }

    @safe_action
    def deduplicate(self) -> Dict[str, int]:
        """Remove duplicate files in the directory based on their hash.
        
        Returns:
            Statistics about the deduplication process.
        """
        self._find_duplicates()
        self._remove_duplicates()

        if self.dry_run:
            self.logger.info(f"Dry run: {len(self.duplicates)} duplicates found.")
        else:
            self.logger.info(f"Deduplication complete: {len(self.duplicates)} duplicates removed.")

        return self.get_statistics()
