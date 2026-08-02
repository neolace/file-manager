"""
Exception hierarchy for the File Manager application.

This module defines a set of custom exceptions used throughout the application
to provide more specific error information and enable better error handling.
"""


class FileManagerError(Exception):
    """Base exception class for all File Manager errors."""

    pass


class ValidationError(FileManagerError):
    """Exception raised for errors in the validation of command arguments."""

    pass


class CommandError(FileManagerError):
    """Exception raised for errors related to command execution."""

    pass


class FileSystemError(FileManagerError):
    """Exception raised for errors related to file system operations."""

    pass


class ArgumentError(ValidationError):
    """Exception raised when required arguments are missing or invalid."""

    pass


class PathError(FileSystemError):
    """Exception raised when a path is invalid or not found."""

    pass


class DirectoryError(PathError):
    """Exception raised when a directory is invalid or not found."""

    pass


class FileError(PathError):
    """Exception raised when a file is invalid or not found."""

    pass


class OperationError(CommandError):
    """Exception raised when a file operation fails."""

    pass


class UnsupportedCommandError(CommandError):
    """Exception raised when an unsupported command is requested."""

    pass
