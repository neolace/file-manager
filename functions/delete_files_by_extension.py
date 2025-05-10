from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import List, Optional, Sequence

# Type aliases for better clarity
PathSequence = Sequence[Path]
ExtensionList = List[str]

@dataclass
class DeletionConfig:
    """Configuration for file deletion process"""
    path: Path
    extensions: ExtensionList
    dry_run: bool = False
    logger: Optional[Logger] = None

class FileDeleter:
    """Handles deletion of files with specified extensions"""
    
    def __init__(self, config: DeletionConfig):
        self.config = config
        self.logger = self._setup_logger()
        self.normalized_extensions = self._normalize_extensions()

    def _setup_logger(self) -> Logger:
        """Initialize or use provided logger"""
        if self.config.logger is None:
            import logging
            return logging.getLogger(__name__)
        return self.config.logger

    def _normalize_extensions(self) -> ExtensionList:
        """Normalize file extensions for comparison"""
        return [ext.lower().lstrip(".") for ext in self.config.extensions]

    def _should_delete_file(self, file_path: Path) -> bool:
        """Check if file should be deleted based on its extension"""
        return (file_path.is_file() and 
                file_path.suffix.lower().lstrip(".") in self.normalized_extensions)

    def _delete_file(self, file_path: Path) -> None:
        """Delete a single file with error handling"""
        try:
            if self.config.dry_run:
                self.logger.info(f"Would delete file: {file_path}")
            else:
                file_path.unlink()
                self.logger.info(f"Deleted file: {file_path}")
        except OSError as e:
            self.logger.error(f"Error deleting file {file_path}: {e}")

    def process_files(self) -> None:
        """Process files in the specified path and delete matching ones"""
        try:
            for file_path in self.config.path.rglob("*"):
                if self._should_delete_file(file_path):
                    self._delete_file(file_path)
        except OSError as e:
            self.logger.error(f"Error accessing {self.config.path}: {e}")

def delete_files_by_extension(
    path: Path,
    extensions: ExtensionList,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Delete all files with the specified extensions in the given path.
    
    Args:
        path: The directory path to search for files
        extensions: List of file extensions to delete (without dots)
        dry_run: If True, only log actions without deleting files
        logger: Logger instance for output
    """
    config = DeletionConfig(
        path=path,
        extensions=extensions,
        dry_run=dry_run,
        logger=logger
    )
    
    deleter = FileDeleter(config)
    deleter.process_files()