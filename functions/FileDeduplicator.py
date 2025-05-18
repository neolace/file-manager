import hashlib
from concurrent.futures import ThreadPoolExecutor
from logging import Logger
from pathlib import Path
from typing import Optional, Iterator, Dict, List, Tuple

from config.Config import Config

# Type aliases
FileHashResult = Tuple[Path, str]


class FileDeduplicator:
    def __init__(
        self,
        directory: str,
        max_workers: int = Config.DEFAULT_MAX_WORKERS,
        logger: Optional[Logger] = None,
        dry_run: bool = False,
    ) -> None:
        self.directory_path = Path(directory)
        self.max_workers = max_workers
        self.logger = self._setup_logger(logger)
        self.dry_run = dry_run
        self.file_hashes: Dict[str, Path] = {}
        self.duplicates: List[Path] = []

    @staticmethod
    def _setup_logger(logger: Optional[Logger]) -> Logger:
        if logger is None:
            import logging

            return logging.getLogger(__name__)
        return logger

    @staticmethod
    def _calculate_file_hash(file: Path) -> FileHashResult:
        """Calculate the hash of a file using a buffered approach.

        Args:
            file: The file to hash.

        Returns:
            A tuple containing the file path and its MD5 hash.
        """
        hasher = hashlib.md5()
        with file.open("rb") as f:
            while chunk := f.read(Config.DEFAULT_BUFFER_SIZE):
                hasher.update(chunk)
        return file, hasher.hexdigest()

    def _get_files(self) -> Iterator[Path]:
        """Get all files in the directory recursively."""
        if not self.directory_path.is_dir():
            raise ValueError(f"{self.directory_path} is not a valid directory.")
        return (file for file in self.directory_path.rglob("*") if file.is_file())

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

    def deduplicate(self) -> None:
        """Remove duplicate files in the directory based on their hash."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for file, file_hash in executor.map(
                self._calculate_file_hash, self._get_files()
            ):
                if file_hash in self.file_hashes:
                    self.duplicates.append(file)
                else:
                    self.file_hashes[file_hash] = file

            for duplicate in self.duplicates:
                self._remove_duplicate(duplicate)

        if self.dry_run:
            self.logger.info(f"Dry run: {len(self.duplicates)} duplicates found.")
