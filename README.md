# File Management Utility

A Python command-line tool for file deduplication, moving files, and other file management operations.

## Features

- Deduplicate files within a specified directory
- Move files from a source directory to a destination directory
- Delete files by extension
- Clean folders of unwanted files
- Delete empty folders
- Delete hidden files
- Rename files based on patterns
- Compress files for archiving
- Configurable logging for all operations
- Dry-run mode to preview changes without applying them
- Extensible command registry to easily add new file management operations

## Requirements

- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

## Usage

All commands are run from the terminal using `main.py`.

### Common Arguments

- `--log <filepath>`: Specifies the path to the log file. Defaults to `app.log` if not specified, or as defined in
  `config/Config.py`.
- `--dry-run`: If present, the script will simulate the actions and log what would happen, but will not make any actual
  changes to the filesystem.
- `--log-level`: Sets the logging level. Default is typically INFO.

### Deduplicate Files

Scans a directory for duplicate files (based on content) and removes them, keeping one copy.

```bash
python main.py --command "deduplicate" --directory "C:\path\to\your\directory" [--log "C:\path\to\your\logfile.log"] [--dry-run] [--max-workers <number>]
```

- `--command "deduplicate"`: Specifies the deduplication command.
- `--directory "C:\path\to\your\directory"`: **Required.** The directory to scan for duplicate files.
- `--max-workers <number>`: (Optional) The maximum number of worker threads to use for processing. Default to 1.

### Move Files

Moves files from a source directory to a destination directory.

```bash
python main.py --command "move" --src-dir "C:\path\to\source_directory" --dst-dir "C:\path\to\destination_directory" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "move"`: Specifies the move command.
- `--src-dir "C:\path\to\source_directory"`: **Required.** The source directory containing files to move.
- `--dst-dir "C:\path\to\destination_directory"`: **Required.** The destination directory where files will be moved.

### Delete Files by Extension

Removes files with specified extensions from a directory.

```bash
python main.py --command "delete_by_extension" --path "C:\path\to\your\directory" --extensions ".tmp,.bak" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "delete_by_extension"`: Specifies the delete by extension command.
- `--path "C:\path\to\your\directory"`: **Required.** The directory to scan for files.
- `--extensions`: **Required.** Comma-separated list of file extensions to delete.

### Clean Folder

Removes temporary and unwanted files from a directory based on predefined patterns.

```bash
python main.py --command "clean_folder" --path "C:\path\to\your\directory" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "clean_folder"`: Specifies the clean folder command.
- `--path "C:\path\to\your\directory"`: **Required.** The directory to clean.

### Delete Empty Folders

Removes empty directories recursively from a specified directory.

```bash
python main.py --command "delete_empty" --path "C:\path\to\your\directory" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "delete_empty"`: Specifies the delete empty folders command.
- `--path "C:\path\to\your\directory"`: **Required.** The directory to scan for empty folders.

### Delete Hidden Files

Removes hidden files from a directory.

```bash
python main.py --command "delete_hidden_files" --path "C:\path\to\your\directory" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "delete_hidden_files"`: Specifies the delete hidden files command.
- `--path "C:\path\to\your\directory"`: **Required.** The directory to scan for hidden files.

### Rename Files

Renames files in a directory based on specified patterns.

```bash
python main.py --command "rename_files" --path "C:\path\to\your\directory" --pattern "old_pattern" --replacement "new_pattern" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "rename_files"`: Specifies the rename files command.
- `--path "C:\path\to\your\directory"`: **Required.** The directory containing files to rename.
- `--pattern`: **Required.** The pattern to match in filenames.
- `--replacement`: **Required.** The replacement pattern.

### Compress Files

Compresses files in a directory into an archive format.

```bash
python main.py --command "compress_files" --path "C:\path\to\your\directory" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "compress_files"`: Specifies the compress files command.
- `--path "C:\path\to\your\directory"`: **Required.** The directory containing files to compress.

## Project Structure

- `main.py`: Main entry point for the application, handles command parsing and execution.
- `config/settings.py`: Contains application-wide configuration settings, constants, and type aliases.
- `functions/`: Module for different file operations.
    - Files for each command implementation (DeduplicateCommand, MoveCommand, etc.)
- `utils/`: Contains utility modules.
    - `parse_arguments.py`: Handles parsing of command-line arguments.
    - `setup_logging.py`: Configures logging for the application.

## Extending

To add new functionality:

1. Define a new command type in `CommandType` enum in `main.py`.
2. Create a new class that implements the `CommandInterface`. This class should include:
    * A `description` property.
    * A `validate(self, args: Namespace)` method to check command-specific arguments.
    * An `execute(self, args: Namespace, logger: logging.Logger)` method to perform the command's action.
3. Register your new command class in the `_commands` dictionary within the `CommandRegistry` class in `main.py`.
4. Update `utils/parse_arguments.py` to include any new command-specific arguments.

## License

MIT License

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes.
