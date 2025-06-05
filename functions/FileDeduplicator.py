import hashlib
import logging
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterator, Dict, List, Tuple, TypeVar

from Interface.CommandInterface import CommandInterface
from config.settings import Config
from functions.exceptions import ArgumentError, FileError, OperationError
from utils.validate_arguments import validate_required_arg, validate_path

# Type aliases
FileHashResult = Tuple[Path, str]
T = TypeVar('T')


class DeduplicateCommand(CommandInterface):
    def __init__(self):
        self.directory = None
        self.duplicates = None
        self.logger = None
        self.file_hashes = None
        self.directory_path = None
        self.dry_run = True
        self.max_workers = 1

    @property
    def description(self) -> str:
        return "Deduplicate files in a directory"

    def validate(self, args: Namespace) -> None:
        # Validate required directory argument
        directory = validate_required_arg(args, 'directory', self.description)

        # Validate that the directory exists and is a directory
        validate_path(directory, must_exist=True, must_be_dir=True)

        # Validate max_workers if provided
        if hasattr(args, 'max_workers') and args.max_workers is not None:
            if not isinstance(args.max_workers, int) or args.max_workers < 1:
                raise ArgumentError(f"'max_workers' must be a positive integer, got {args.max_workers}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        self.directory = args.directory
        self.max_workers = args.max_workers
        self.logger = logger
        self.dry_run = args.dry_run
        self.file_hashes: Dict[str, Path] = {}
        self.duplicates: List[Path] = []

        self._deduplicate()

    def _calculate_file_hash(self, file: Path) -> FileHashResult:
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
            self.logger.error(f"File: {file.name} - Encoding error: {e}")
            raise FileError(f"Encoding error when processing file {file.name}: {e}") from e
        return file, hasher.hexdigest()

    def _get_files(self) -> Iterator[Path]:
        """Get all files in the directory recursively."""
        # Validate that the directory exists and is a directory
        directory_path = validate_path(self.directory, must_exist=True, must_be_dir=True)
        return (file for file in directory_path.rglob("*") if file.is_file())

    def _find_duplicates(self) -> None:
        """Find duplicate files based on their hash."""
        self.file_hashes.clear()
        self.duplicates.clear()

        self.logger.info(f"Scanning for files in {self.directory}")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Process files in parallel
            for file, file_hash in executor.map(
                    lambda f: self._calculate_file_hash(f), self._get_files()
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
            raise OperationError(f"Failed to remove duplicate file {duplicate}: {e}") from e

    def _remove_duplicates(self) -> None:
        """Remove all identified duplicate files."""
        for duplicate in self.duplicates:
            self._remove_duplicate(duplicate)

    def _get_statistics(self) -> Dict[str, int]:
        """Return statistics about the deduplication process.

        Returns:
            A dictionary with statistics like total files, unique files, and duplicates.
        """
        return {
            "total_files": len(self.file_hashes) + len(self.duplicates),
            "unique_files": len(self.file_hashes),
            "duplicates": len(self.duplicates)
        }


    def _deduplicate(self) -> Dict[str, int]:
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

        return self._get_statistics()
