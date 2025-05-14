from logging import Logger
from pathlib import Path
from typing import List, Optional, Union, TypeAlias, Dict, Callable

from delete_all_files_folders_within_folder import (
    delete_all_files_folders_within_folder,
)
from delete_all_hidden_folders import delete_all_hidden_folders
from delete_empty_folders import delete_empty_folders
from delete_files_by_extension import delete_files_by_extension
from utils.setup_logging import setup_logging

# Type aliases for better readability
PathLike: TypeAlias = Union[str, Path]
ExtensionList: TypeAlias = List[str]
ExcludedNames: TypeAlias = List[str]


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
        self._operation_handlers: Dict[str, Callable] = {
            "delete_by_extension": self._handle_delete_by_extension,
            "clean_folder": self._handle_clean_folder,
            "delete_empty": self._handle_delete_empty,
            "delete_hidden": self._handle_delete_hidden,
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

    def execute(
        self,
        extensions: Optional[ExtensionList] = None,
        excluded_names: Optional[ExcludedNames] = None,
        dry_run: bool = False,
        recursive: bool = True,
    ) -> Optional[int]:
        try:
            handler = self._operation_handlers[self.operation]
            return handler(extensions, excluded_names, dry_run, recursive)
        except Exception as e:
            self.logger.error(f"Error during {self.operation}: {str(e)}")
            raise

    def _handle_delete_by_extension(
        self,
        extensions: Optional[ExtensionList],
        dry_run: bool,
    ) -> None:
        delete_files_by_extension(
            path=self.path, extensions=extensions, dry_run=dry_run, logger=self.logger
        )
        return None

    def _handle_clean_folder(
        self,
        excluded_names: Optional[ExcludedNames],
        dry_run: bool,
    ) -> None:
        delete_all_files_folders_within_folder(
            directory_path=self.path,
            excluded_names=excluded_names,
            dry_run=dry_run,
            logger=self.logger,
        )
        return None

    def _handle_delete_empty(
        self,
        dry_run: bool,
        recursive: bool,
    ) -> int:
        return delete_empty_folders(
            path=self.path, dry_run=dry_run, recursive=recursive, logger=self.logger
        )

    def _handle_delete_hidden(
        self,
        excluded_names: Optional[ExcludedNames],
        dry_run: bool,
    ) -> None:
        delete_all_hidden_folders(
            path=self.path,
            excluded_names=excluded_names,
            dry_run=dry_run,
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

    return manager.execute(
        extensions=extensions,
        excluded_names=excluded_names,
        dry_run=dry_run,
        recursive=recursive,
    )
