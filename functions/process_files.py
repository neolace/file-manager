from pathlib import Path
from typing import List, Optional, Union

from delete_all_files_folders_within_folder import (
    delete_all_files_folders_within_folder,
)
from delete_all_hidden_folders import delete_all_hidden_folders
from delete_empty_folders import delete_empty_folders
from delete_files_by_extension import delete_files_by_extension
from utils.setup_logging import setup_logging


def process_files(
    operation: str,
    path: Union[str, Path],
    *,
    extensions: Optional[List[str]] = None,
    excluded_names: Optional[List[str]] = None,
    dry_run: bool = False,
    recursive: bool = True,
    log_file: Optional[Union[str, Path]] = None,
) -> Optional[int]:
    """
    Process files according to the specified operation.

    Args:
        operation: The operation to perform. One of:
            - 'delete_by_extension': Delete files with specific extensions
            - 'clean_folder': Delete all files and folders within a directory
            - 'delete_empty': Delete empty folders
            - 'delete_hidden': Delete hidden folders
        path: The directory path to process
        extensions: List of file extensions to process (required for delete_by_extension)
        excluded_names: List of names to exclude from deletion
        dry_run: If True, only simulate operations without making changes
        recursive: Whether to process subdirectories recursively (for delete_empty)
        log_file: Path to the log file. If None, logs to console only

    Returns:
        int: Number of items processed (for operations that track count)
        None: For operations that don't return a count

    Raises:
        ValueError: If invalid operation specified or missing required parameters
    """
    # Convert path to Path object
    path = Path(path)

    # Setup logging
    logger = setup_logging(Path(log_file) if log_file else Path("file_operations.log"))

    # Validate operation
    valid_operations = {
        "delete_by_extension",
        "clean_folder",
        "delete_empty",
        "delete_hidden",
    }

    if operation not in valid_operations:
        raise ValueError(
            f"Invalid operation. Must be one of: {', '.join(valid_operations)}"
        )

    # Validate parameters based on operation
    if operation == "delete_by_extension" and not extensions:
        raise ValueError(
            "extensions parameter is required for delete_by_extension operation"
        )

    try:
        if operation == "delete_by_extension":
            delete_files_by_extension(
                path=path, extensions=extensions, dry_run=dry_run, logger=logger
            )
            return None

        elif operation == "clean_folder":
            delete_all_files_folders_within_folder(
                directory_path=path,
                excluded_names=excluded_names,
                dry_run=dry_run,
                logger=logger,
            )
            return None

        elif operation == "delete_empty":
            return delete_empty_folders(
                path=path, dry_run=dry_run, recursive=recursive, logger=logger
            )

        elif operation == "delete_hidden":
            delete_all_hidden_folders(
                path=path, excluded_names=excluded_names, dry_run=dry_run, logger=logger
            )
            return None

    except Exception as e:
        logger.error(f"Error during {operation}: {str(e)}")
        raise


if __name__ == "__main__":
    import click

    @click.command()
    @click.argument(
        "operation",
        type=click.Choice(
            ["delete_by_extension", "clean_folder", "delete_empty", "delete_hidden"]
        ),
    )
    @click.argument("path", type=click.Path(exists=True))
    @click.option(
        "--extensions", "-e", multiple=True, help="File extensions to process"
    )
    @click.option(
        "--excluded", "-x", multiple=True, help="Names to exclude from deletion"
    )
    @click.option(
        "--dry-run", is_flag=True, help="Simulate operations without making changes"
    )
    @click.option("--no-recursive", is_flag=True, help="Disable recursive processing")
    @click.option("--log-file", type=click.Path(), help="Path to log file")
    def main(
        operation: str,
        path: str,
        extensions: tuple,
        excluded: tuple,
        dry_run: bool,
        no_recursive: bool,
        log_file: Optional[str],
    ) -> None:
        """Process files based on the specified operation."""
        try:
            result = process_files(
                operation=operation,
                path=path,
                extensions=list(extensions) if extensions else None,
                excluded_names=list(excluded) if excluded else None,
                dry_run=dry_run,
                recursive=not no_recursive,
                log_file=log_file,
            )

            if result is not None:
                click.echo(f"Operation completed. Processed {result} items.")
            else:
                click.echo("Operation completed successfully.")

        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
            raise click.Abort()

    main()
