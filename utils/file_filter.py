"""
Utility class for filtering files based on various criteria.

This module provides a FileFilter class that can be used to filter files
based on extensions, names, patterns, and other criteria.
"""

from pathlib import Path
from typing import List, Optional, Iterator, Union, Set


class FileFilter:
    """
    A utility class for filtering files based on various criteria.
    """

    def __init__(self, 
                 extensions: Optional[List[str]] = None,
                 excluded_names: Optional[List[str]] = None,
                 excluded_extensions: Optional[List[str]] = None,
                 min_size: Optional[int] = None,
                 max_size: Optional[int] = None,
                 include_hidden: bool = True):
        """
        Initialize a FileFilter with the specified criteria.

        Args:
            extensions: A list of file extensions to include (without the dot).
            excluded_names: A list of file names or patterns to exclude.
            excluded_extensions: A list of file extensions to exclude (without the dot).
            min_size: The minimum file size in bytes.
            max_size: The maximum file size in bytes.
            include_hidden: Whether to include hidden files.
        """
        self.extensions = self._normalize_extensions(extensions) if extensions else None
        self.excluded_names = excluded_names
        self.excluded_extensions = self._normalize_extensions(excluded_extensions) if excluded_extensions else None
        self.min_size = min_size
        self.max_size = max_size
        self.include_hidden = include_hidden

    @staticmethod
    def _normalize_extensions(extensions: List[str]) -> Set[str]:
        """
        Normalize a list of extensions by removing dots and converting to lowercase.

        Args:
            extensions: A list of file extensions.

        Returns:
            A set of normalized extensions.
        """
        return {ext.lower().lstrip('.') for ext in extensions if ext}

    def matches_extension(self, file_path: Path) -> bool:
        """
        Check if a file matches the extension criteria.

        Args:
            file_path: The file path to check.

        Returns:
            True if the file matches the extension criteria, False otherwise.
        """
        if not self.extensions:
            return True

        ext = file_path.suffix.lower().lstrip('.')
        return ext in self.extensions

    def matches_excluded_extension(self, file_path: Path) -> bool:
        """
        Check if a file matches the excluded extension criteria.

        Args:
            file_path: The file path to check.

        Returns:
            True if the file matches the excluded extension criteria, False otherwise.
        """
        if not self.excluded_extensions:
            return False

        ext = file_path.suffix.lower().lstrip('.')
        return ext in self.excluded_extensions

    def matches_excluded_name(self, file_path: Path) -> bool:
        """
        Check if a file matches the excluded name criteria.

        Args:
            file_path: The file path to check.

        Returns:
            True if the file matches the excluded name criteria, False otherwise.
        """
        if not self.excluded_names:
            return False

        return any(excluded in file_path.name for excluded in self.excluded_names)

    def matches_size(self, file_path: Path) -> bool:
        """
        Check if a file matches the size criteria.

        Args:
            file_path: The file path to check.

        Returns:
            True if the file matches the size criteria, False otherwise.
        """
        if not self.min_size and not self.max_size:
            return True

        size = file_path.stat().st_size
        if self.min_size and size < self.min_size:
            return False
        if self.max_size and size > self.max_size:
            return False
        return True

    def matches_hidden(self, file_path: Path) -> bool:
        """
        Check if a file matches the hidden criteria.

        Args:
            file_path: The file path to check.

        Returns:
            True if the file matches the hidden criteria, False otherwise.
        """
        if self.include_hidden:
            return True

        return not file_path.name.startswith('.')

    def matches(self, file_path: Path) -> bool:
        """
        Check if a file matches all the criteria.

        Args:
            file_path: The file path to check.

        Returns:
            True if the file matches all the criteria, False otherwise.
        """
        if not file_path.is_file():
            return False

        if self.matches_excluded_name(file_path):
            return False

        if self.matches_excluded_extension(file_path):
            return False

        if not self.matches_extension(file_path):
            return False

        if not self.matches_size(file_path):
            return False

        if not self.matches_hidden(file_path):
            return False

        return True

    def filter_files(self, directory: Union[str, Path], recursive: bool = True) -> List[Path]:
        """
        Filter files in a directory based on the criteria.

        Args:
            directory: The directory to filter files in.
            recursive: Whether to recursively search subdirectories.

        Returns:
            A list of file paths that match the criteria.
        """
        directory_path = Path(directory)
        if not directory_path.is_dir():
            raise ValueError(f"Not a directory: {directory}")

        if recursive:
            files = directory_path.rglob('*')
        else:
            files = directory_path.glob('*')

        return [file_path for file_path in files if self.matches(file_path)]

    def filter_files_iterator(self, directory: Union[str, Path], recursive: bool = True) -> Iterator[Path]:
        """
        Filter files in a directory based on the criteria, returning an iterator.

        Args:
            directory: The directory to filter files in.
            recursive: Whether to recursively search subdirectories.

        Returns:
            An iterator of file paths that match the criteria.
        """
        directory_path = Path(directory)
        if not directory_path.is_dir():
            raise ValueError(f"Not a directory: {directory}")

        if recursive:
            files = directory_path.rglob('*')
        else:
            files = directory_path.glob('*')

        for file_path in files:
            if self.matches(file_path):
                yield file_path