"""
Utility functions for validating command arguments.

This module provides functions for validating different types of command arguments,
such as paths, extensions, patterns, etc.
"""

from argparse import Namespace
from pathlib import Path
from typing import List, Optional, Any, Union

from functions.exceptions import ArgumentError, PathError, DirectoryError, FileError


def validate_required_arg(args: Namespace, arg_name: str, command_description: str) -> Any:
    """
    Validate that a required argument is present.

    Args:
        args: The command arguments.
        arg_name: The name of the argument to validate.
        command_description: The description of the command.

    Returns:
        The value of the argument.

    Raises:
        ArgumentError: If the argument is not present.
    """
    value = getattr(args, arg_name, None)
    if not value:
        raise ArgumentError(f"'{arg_name}' argument is required for the '{command_description}' command.")
    return value


def validate_path(path: Union[str, Path], must_exist: bool = True, must_be_dir: bool = False,
                  must_be_file: bool = False, create_if_not_exists: bool = False) -> Path:
    """
    Validate a path.

    Args:
        path: The path to validate.
        must_exist: Whether the path must exist.
        must_be_dir: Whether the path must be a directory.
        must_be_file: Whether the path must be a file.
        create_if_not_exists: Whether to create the path if it doesn't exist.

    Returns:
        The validated path as a Path object.

    Raises:
        PathError: If the path is invalid.
        DirectoryError: If the path is not a directory when must_be_dir is True.
        FileError: If the path is not a file when must_be_file is True.
    """
    try:
        path_obj = Path(path)
        
        if must_exist and not path_obj.exists():
            if create_if_not_exists:
                if must_be_dir:
                    path_obj.mkdir(parents=True, exist_ok=True)
                else:
                    path_obj.parent.mkdir(parents=True, exist_ok=True)
                    path_obj.touch(exist_ok=True)
            else:
                raise PathError(f"Path not found: {path}")
        
        if must_be_dir and path_obj.exists() and not path_obj.is_dir():
            raise DirectoryError(f"Path is not a directory: {path}")
        
        if must_be_file and path_obj.exists() and not path_obj.is_file():
            raise FileError(f"Path is not a file: {path}")
        
        return path_obj
    except Exception as e:
        if isinstance(e, (PathError, DirectoryError, FileError)):
            raise
        raise PathError(f"Invalid path: {path}") from e


def validate_extensions(extensions: Optional[str]) -> List[str]:
    """
    Validate and parse a comma-separated list of file extensions.

    Args:
        extensions: A comma-separated list of file extensions.

    Returns:
        A list of validated file extensions.

    Raises:
        ArgumentError: If the extensions are invalid.
    """
    if not extensions:
        return []
    
    # Parse the extensions
    ext_list = [ext.strip().lower() for ext in extensions.split(',') if ext.strip()]
    
    # Validate each extension
    for ext in ext_list:
        if not ext:
            continue
        
    return ext_list


def validate_pattern(pattern: Optional[str]) -> str:
    """
    Validate a pattern for file operations.

    Args:
        pattern: The pattern to validate.

    Returns:
        The validated pattern.

    Raises:
        ArgumentError: If the pattern is invalid.
    """
    if not pattern:
        raise ArgumentError("Pattern cannot be empty.")
    
    return pattern