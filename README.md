# File Manager

A Python utility for efficient file management, cleaning, and organization.

## Features

- **Move files**: Transfer files between directories based on type
- **Copy files**: Duplicate files from one location to another
- **Delete files**: Remove files matching specific criteria
- **Clean directories**: Remove temporary or unwanted files
- **Extract archives**: Unpack compressed files with 7zip support
- **Find duplicates**: Identify and manage duplicate files
- **Organize by date**: Sort files into folders based on date metadata
- **Search files**: Find files containing specific text
- **Process extensions**: Perform operations based on file extensions

## Installation

```bash
# Clone the repository
git clone https://github.com/neolace/file-manager.git
cd file-manager

# Install the package
pip install -e .

# For development dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Commands

```bash
# Move PDF files
file-manager move --source /path/source --target /path/target --type pdf

# Delete JPG files (dry run)
file-manager delete --path /test/path --type jpg --dry-run

# Remove files with "temp" in the name (verbose)
file-manager remove --path /test/path --name temp --verbose

# Clean a directory
file-manager clean --path /test/path --all

# Extract archives
file-manager extract --path /archives --7zip /path/to/7z.exe

# Copy MP3 files (dry run and verbose)
file-manager copy --source /src --target /dest --type mp3 --dry-run --verbose

# Find duplicate files
file-manager find-dupes --path /test/folder

# Organize files by date
file-manager organize-date --source /photos --target /archive --format "%Y/%m/%d"

# Search within files
file-manager search --path /docs --text "important" --extensions txt md doc

# Process files by extension
file-manager process-extensions --path /files --dry-run
```

### Command Line Options

Most commands support the following options:

- `--dry-run`: Show what would be done without making changes
- `--verbose`: Display detailed information during execution

## Development

### Testing

```bash
# Run tests with pytest
pytest

# Run linting
pylint file_manager

# Format code
black file_manager
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
