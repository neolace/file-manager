# File Management Utility

A Python command-line tool for file deduplication, moving files, and other file management operations.

## Features

- Deduplicate files within a specified directory.
- Move files from a source directory to a destination directory.
- Configurable logging for all operations.
- Dry-run mode to preview changes without applying them.
- Extensible command registry to easily add new file management operations.

## Requirements

- Python 3.8+
- Install dependencies: `pip install -r requirements.txt` (Assuming you have a `requirements.txt` file)

## Usage

All commands are run from the terminal using `main.py`.

### Common Arguments

- `--log <filepath>`: Specifies the path to the log file. Defaults to `app.log` if not specified, or as defined in
  `config/Config.py`.
- `--dry-run`: If present, the script will simulate the actions and log what would happen, but will not make any actual
  changes to the filesystem.

### Deduplicate Files

Scans a directory for duplicate files (based on content) and removes them, keeping one copy.

```bash
python main.py --command "deduplicate" --directory "C:\path\to\your\directory" [--log "C:\path\to\your\logfile.log"] [--dry-run] [--max-workers <number>]
```

- `--command "deduplicate"`: Specifies the deduplication command.
- `--directory "C:\path\to\your\directory"`: **Required.** The directory to scan for duplicate files.
- `--max-workers <number>`: (Optional) The maximum number of worker threads to use for processing. Defaults to 1.

### Move Files

Moves files from a source directory to a destination directory. (Note: The current implementation of
`MoveCommand.execute` is a placeholder and needs to be filled out).

```bash
python main.py --command "move" --src-dir "C:\path\to\source_directory" --dst-dir "C:\path\to\destination_directory" [--log "C:\path\to\your\logfile.log"] [--dry-run]
```

- `--command "move"`: Specifies the move command.
- `--src-dir "C:\path\to\source_directory"`: **Required.** The source directory containing files to move.
- `--dst-dir "C:\path\to\destination_directory"`: **Required.** The destination directory where files will be moved.

## Project Structure

- `main.py`: Main entry point for the application, handles command parsing and execution.
- `config/Config.py`: Contains application-wide configuration settings, constants, and type aliases.
- `functions/`: Module for different file operations.
    - `FileDeduplicator.py`: Implements the logic for file deduplication.
- `utils/`: Contains utility modules.
    - `parse_arguments.py`: Handles parsing of command-line arguments.
    - `setup_logging.py`: Configures logging for the application.
- `README.md`: This file.

## Extending

To add new functionality:

1. Define a new command type in `CommandType` enum in `main.py`.
2. Create a new class that implements the `CommandInterface` (from `main.py`). This class should include:
    * A `description` property.
    * A `validate(self, args: Namespace)` method to check command-specific arguments.
    * An `execute(self, args: Namespace, logger: logging.Logger)` method to perform the command's action.
3. Register your new command class in the `_commands` dictionary within the `CommandRegistry` class in `main.py`.
4. Update `utils/parse_arguments.py` to include any new command-specific arguments.

## License

MIT License

```
