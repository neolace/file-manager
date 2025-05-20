import shutil
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Optional, Dict

from config.Config import (
    ExtensionList,
    ExcludedNames,
    PathLike,
    Config,
    OperationHandler,
)
from delete_all_hidden_folders import delete_all_hidden_folders
from delete_empty_folders import delete_empty_folders
from delete_files_by_extension import delete_files_by_extension
from utils.setup_logging import setup_logging


@dataclass
class OperationConfig:
    """Configuration for file operations"""

    extensions: Optional[ExtensionList] = None
    excluded_names: Optional[ExcludedNames] = None
    dry_run: bool = False
    recursive: bool = True


def get_default_logger() -> Logger:
    """Create and return a default logger."""
    import logging

    return logging.getLogger(__name__)


def is_valid_directory(path: Path) -> bool:
    """Check if the given path is a valid directory."""
    return path.exists() and path.is_dir()


class FileDeleter:
    """Handles file deletion operations"""

    @staticmethod
    def delete_item(item: Path, logger: Logger) -> None:
        """Delete a file system item and log the action."""
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
                logger.info(Config.get_log_message("DELETED_FILE").format(item))
            elif item.is_dir():
                shutil.rmtree(item)
                logger.info(Config.get_log_message("DELETED_DIR").format(item))
        except Exception as e:
            logger.error(Config.get_log_message("DELETE_ERROR").format(item, e))


class FileOperationManager:
    VALID_OPERATIONS = {
        "delete_by_extension",
        "clean_folder",
        "delete_empty",
        "delete_hidden",
    }

    def __init__(self, operation: str, path: PathLike, logger: Logger):
        self.operation = operation
        self.path = Path(path)
        self.logger = logger
        self.file_deleter = FileDeleter()
        self._operation_handlers: Dict[str, OperationHandler] = {
            "delete_by_extension": self._handle_file_deletion_by_extension,
            "clean_folder": self._handle_folder_cleanup,
            "delete_empty": self._handle_empty_folder_deletion,
            "delete_hidden": self._handle_hidden_folder_deletion,
        }

    def validate_operation(self) -> None:
        if self.operation not in self.VALID_OPERATIONS:
            raise ValueError(
                f"Invalid operation. Must be one of: {', '.join(self.VALID_OPERATIONS)}"
            )

    def validate_extensions(self, extensions: Optional[ExtensionList]) -> None:
        if self.operation == "delete_by_extension" and not extensions:
            raise ValueError(
                "extensions parameter is required for delete_by_extension operation"
            )

    def execute(self, config: OperationConfig) -> Optional[int]:
        try:
            handler = self._operation_handlers[self.operation]
            return handler(**config.__dict__)
        except Exception as e:
            self.logger.error(f"Error during {self.operation}: {str(e)}")
            raise

    def _handle_file_deletion_by_extension(self, **kwargs) -> None:
        delete_files_by_extension(
            path=self.path,
            extensions=kwargs["extensions"],
            dry_run=kwargs["dry_run"],
            logger=self.logger,
        )
        return None

    def _handle_folder_cleanup(self, **kwargs) -> None:
        if not is_valid_directory(self.path):
            self.logger.warning(Config.get_log_message("INVALID_DIR").format(self.path))
            return None

        for item in self.path.iterdir():
            if item.name not in (kwargs["excluded_names"] or []):
                if not kwargs["dry_run"]:
                    self.file_deleter.delete_item(item, self.logger)
                else:
                    self.logger.info(
                        Config.get_log_message("WOULD_DELETE").format(item)
                    )
        return None

    def _handle_empty_folder_deletion(self, **kwargs) -> int:
        return delete_empty_folders(
            path=self.path,
            dry_run=kwargs["dry_run"],
            recursive=kwargs["recursive"],
            logger=self.logger,
        )

    def _handle_hidden_folder_deletion(self, **kwargs) -> None:
        delete_all_hidden_folders(
            path=self.path,
            excluded_names=kwargs["excluded_names"],
            dry_run=kwargs["dry_run"],
            logger=self.logger,
        )
        return None


def process_files(
        operation: str,
        path: PathLike,
        *,
        extensions: Optional[ExtensionList] = None,
        excluded_names: Optional[ExcludedNames] = None,
        dry_run: bool = False,
        recursive: bool = True,
        log_file: Optional[PathLike] = None,
) -> Optional[int]:
    logger = setup_logging(Path(log_file) if log_file else Path("file_operations.log"))
    manager = FileOperationManager(operation, path, logger)
    manager.validate_operation()
    manager.validate_extensions(extensions)

    config = OperationConfig(
        extensions=extensions,
        excluded_names=excluded_names,
        dry_run=dry_run,
        recursive=recursive,
    )
    return manager.execute(config)
