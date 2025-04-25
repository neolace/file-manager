# File Manager

A Python utility for efficient file management, cleaning, and organization.

## Overview

This tool helps manage directories by:

- Processing and organizing files by type
- Cleaning up empty folders
- Removing specific folder types (e.g., node_modules, pip)
- Deleting unwanted files while preserving specified file types

## Project Structure

```
file-manager/
├── config.py                  # Configuration settings
├── main.py                    # Main entry point
├── setup.py                   # Package installation
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
└── helpers/                   # Utility functions
    ├── __init__.py            # Package exports
    ├── copy_files_by_extension.py
    ├── delete_all_files_folders_within_folder.py
    ├── delete_all_hidden_folders.py
    ├── delete_dot_folders_recursive.py
    ├── delete_empty_folders.py
    ├── delete_files_by_extension.py
    ├── delete_files_by_name.py
    ├── drop_all_empty_folders.py
    ├── find_first_char.py
    ├── process_files.py
    └── setup_logging.py
```

## Features

- **File Processing**: Move and organize files by type
- **Directory Cleaning**: Remove empty directories
- **Targeted Deletion**: Delete specific folders by name or pattern
- **Hidden Folder Management**: Remove dot folders (folders starting with ".")
- **Dry Run Mode**: Preview changes without modifying files
- **Detailed Logging**: Track all operations with configurable logging

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/file-manager.git
   cd file-manager
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install as a package (optional):
   ```bash
   pip install -e .
   ```

## Usage

### Basic Usage

```bash
python main.py
```

### Command Line Options

```bash
python main.py --dry-run --src "C:/path/to/source" --dst "C:/path/to/destination" --log "C:/path/to/logfile.log"
```

Options:

- `--dry-run`: Run without making changes (preview mode)
- `--src`: Source directory path
- `--dst`: Destination directory path
- `--log`: Custom log file path

### Configuration

Edit `config.py` to customize:

- File types to keep (`FILE_TYPES_TO_KEEP`)
- Folders to remove (`FOLDERS_TO_REMOVE`)
- Default paths

## Examples

### Clean Up a Directory

```python
from pathlib import Path
from helpers.delete_all_files_folders_within_folder import delete_all_files_folders_within_folder
from config import FILE_TYPES_TO_KEEP

# Keep only specified file types in a directory
delete_all_files_folders_within_folder(
    Path("C:/Users/Documents"),
    dry_run=False
)
```

### Remove Empty Folders

```python
from pathlib import Path
from helpers import drop_all_empty_folders

# Clean up empty directories
drop_all_empty_folders(Path("C:/Users/Downloads"))
```

### Delete Dot Folders

```python
from pathlib import Path
from helpers import delete_dot_folders_recursive

# Remove all hidden folders (e.g., .git, .vscode)
delete_dot_folders_recursive(Path("C:/Users/Projects"))
```

## License

[MIT License](LICENSE)
