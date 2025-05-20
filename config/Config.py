from enum import Enum
from pathlib import Path
from typing import Final, List, Optional, Union, TypeAlias, TypeVar, Callable, Sequence

import config.fm_FileType

PathLike: TypeAlias = Union[str, Path]
ExtensionList: TypeAlias = List[str]
ExcludedNames: TypeAlias = List[str]
OperationHandler: TypeAlias = Callable[..., Optional[int]]
PathSequence = Sequence[Path]


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Config:
    """Application configuration settings."""

    EXCLUDED_FOLDERS: Final[List[str]] = ["node_modules"]
    DEFAULT_FONT: Final[str] = "slant"
    DEFAULT_ENCODING: Final[str] = "utf-8"
    DEFAULT_BUFFER_SIZE: Final = 65536
    DEFAULT_MAX_WORKERS: Final = 1
    DEFAULT_LOG_FILENAME: Final = Path("default.log")
    DEFAULT_LOG_PATH: Final[Path] = Path("app.log")
    HIDDEN_PREFIX: Final = "."
    DEFAULT_LOG_LEVEL: Final = LogLevel.INFO

    # Constants for log messages
    LOG_WOULD_APPLY: Final = "Would apply action to: {}"
    LOG_APPLIED: Final = "Applied action to: {}"
    LOG_ERROR: Final = "Error applying action to {}: {}"
    PATH_NOT_EXIST_ERROR: Final = "Path does not exist: {}"

    # Constants for error messages
    ERROR_NO_EXTENSIONS: Final = "No file extensions provided."
    ERROR_PATH_NOT_EXISTS: Final = "Root path does not exist: {}"
    ERROR_NOT_DIRECTORY: Final = "Root path is not a directory: {}"
    T = TypeVar("T")
    ERROR_MESSAGE_FORMAT: Final = "Error executing {}: {}"
    EMPTY_RESULT: Final = ""
    COMMAND_DEDUPLICATE: Final = "deduplicate"
    ARG_LOG: Final = "--log"
    ARG_DRY_RUN: Final = "--dry-run"
    ARG_PATH: Final = "--path"
    SEVEN_ZIP_ARCHIVE_EXT: Final = "*.7z"
    EXTRACT_CMD: Final = "x"
    FORCE_YES_FLAG: Final = "-y"

    # Environment-dependent paths with defaults
    DEFAULT_SRC_PATH = EMPTY_RESULT
    DEFAULT_DST_PATH = EMPTY_RESULT

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Returns a list of all supported file extensions."""
        return [ft.value for ft in config.fm_fileTypeList]

    @classmethod
    def get_log_message(cls, key: str) -> str:
        """
        Returns a specific log message template by key.

        Args:
            key: The message key to retrieve

        Returns:
            The message template string or empty string if the key is not found
        """
        log_messages = {
            "INVALID_DIR": "Directory does not exist or is not a directory: {}",
            "SKIP_EXCLUDED": "Skipping excluded item: {}",
            "WOULD_DELETE": "Would delete: {}",
            "DELETED_FILE": "Deleted file: {}",
            "DELETED_DIR": "Deleted directory: {}",
            "DELETE_ERROR": "Error deleting {}: {}",
            "SOURCE_NOT_FOUND": "Source folder does not exist: {}",
            "FILES_FOUND": "Found {} .{} files to move",
            "TARGET_CREATED": "Created target directory: {}",
            "MOVE_SUCCESS": "Moved {} to {}",
            "MOVE_FAILURE": "Failed to move {} to {}: {}",
            "WOULD_MOVE": "Would move {} to {}",
            "SUMMARY": "{} {} .{} files",
        }
        return log_messages.get(key, "")
