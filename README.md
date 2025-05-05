# File Manager

A command-line utility for bulk file management operations.

## Overview

File Manager is a Python utility tool that provides various file management functions like deduplication, cleaning up
directories, organizing files by extension, and more. It's designed for users who need to perform batch operations on
large collections of files.

## Features

- **Deduplication**: Remove duplicate files from directories
- **File organization**: Copy files by extension to organized directories
- **Directory cleanup**:
    - Delete empty folders
    - Delete files by specific extensions
    - Delete hidden folders (starting with '.')
    - Clean contents of specified folders
- **Configuration**: Easy to configure default settings

## Installation

### Prerequisites

- Python 3.8+
- No external dependencies required (uses standard library)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/username/file-manager.git
   cd file-manager
   ```

2. Run the application:
   ```
   python main.py [command] [options]
   ```

## Usage

### Command Line Options

```
python main.py [--src SOURCE] [--dst DESTINATION] [--log LOGFILE] [--dry-run] <command>
```

Options:

- `--src`: Source directory path (default: configured in settings)
- `--dst`: Destination directory path (default: configured in settings)
- `--log`: Log file path (default: file_manager.log)
- `--dry-run`: Run without making changes (simulation mode)

Commands:

- `deduplicate`: Remove duplicate files
  ```
  python main.py deduplicate /path/to/directory --dry-run
  ```

### Examples

Remove duplicate files:

```
python main.py --src /path/to/source deduplicate
```

Copy all image files to another directory:

```
python main.py --src /path/to/source --dst /path/to/destination copy-by-extension jpg jpeg png
```

Delete all empty folders:

```
python main.py --src /path/to/source delete-empty-folders
```

### Extending Functionality

You can easily extend the File Manager by adding new functions to the `functions/` directory.

## Configuration

The application settings can be configured in `config/settings.py`:

- `FILE_TYPES_TO_KEEP`: File extensions to keep during cleanup operations
- `FOLDERS_TO_REMOVE`: Folder names to target for removal
- `DEFAULT_SRC_PATH`, `DEFAULT_DST_PATH`, `DEFAULT_LOG_PATH`: Default paths for operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-function`)
3. Commit your changes (`git commit -m 'Add new file management function'`)
4. Push to the branch (`git push origin feature/new-function`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Python's PathLib for modern file system operations
- Python's concurrent.futures for multi-threading capabilities
