# File Manager CLI

A command-line interface tool for file management operations such as deduplication and file moving/organization.

## Features

- **File Deduplication**: Remove duplicate files from a directory
- **File Organization**: Move files from source to destination directories with filtering by file types
- **Dry Run Mode**: Preview changes without making actual modifications
- **Detailed Logging**: Comprehensive logging of all operations

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/file-manager.git
cd file-manager

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Deduplicate Files

Remove duplicate files from a directory:

```bash
python main.py deduplicate --directory /path/to/folder [--dry-run] [--log logfile.log]
```

### Move Files

Move files from source to destination with optional filtering:

```bash
python main.py move --src /path/to/source --dst /path/to/destination [--file-types jpg png pdf] [--dry-run] [--log logfile.log]
```

### Options

- `--directory`: Directory to scan for duplicates
- `--src`: Source directory for file operations
- `--dst`: Destination directory for file operations
- `--file-types`: List of file extensions to process (e.g., jpg png pdf)
- `--dry-run`: Preview changes without making actual modifications
- `--log`: Custom log file path (default: uses value from config)

## Project Structure

```
file-manager/
├── config.py              # Application configuration settings
├── main.py                # Main entry point
├── functions/
│   ├── deduplicate.py     # File deduplication functionality
│   └── process_files.py   # File processing and moving functionality
└── utils/
    ├── parse_arguments.py # Command line argument parsing
    └── setup_logging.py   # Logging configuration
```

## Configuration

Configuration settings can be adjusted in the `config.py` file:

- `DEFAULT_LOG_PATH`: Default log file location
- Other application-specific settings

## Development

### Adding New Commands

To add a new command:

1. Add argument handling in parse_arguments.py
2. Create a validation function in main.py if needed
3. Implement the command handler function in main.py
4. Add the command to the `command_handlers` dictionary

## License

MIT License