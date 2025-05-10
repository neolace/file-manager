from pathlib import Path
from typing import List, Optional

def find_files(
    directory: Path,
    pattern: str = "*",
    extensions: Optional[List[str]] = None
) -> List[Path]:
    """
    Find all files in a directory and its subdirectories with optional filtering.
    
    Args:
        directory (Path): The root directory to search
        pattern (str): Glob pattern for file matching (default: "*")
        extensions (List[str], optional): List of file extensions to filter by (e.g. [".txt", ".py"])
    
    Returns:
        List[Path]: List of matching file paths
    
    Raises:
        ValueError: If directory doesn't exist or is not a directory
    """
    if not directory.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    def _matches_extension(file: Path) -> bool:
        if not extensions:
            return True
        return file.suffix.lower() in [ext.lower() for ext in extensions]
    
    return [
        file for file in directory.rglob(pattern)
        if file.is_file() and _matches_extension(file)
    ]