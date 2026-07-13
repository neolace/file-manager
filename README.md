# File Manager

A command-line file management utility for common house-keeping tasks such as
deduplicating files, deleting files by extension, cleaning folders, removing
empty directories, deleting hidden files, and compressing files into a ZIP
archive.

The tool is built around a simple, extensible command pattern: each operation is
a self-contained command that validates its own arguments and executes against a
shared logger, with first-class support for a `--dry-run` mode so you can preview
every action before anything touches disk.

## Features

- **Deduplicate** – Find and remove duplicate files using MD5 content hashing,
  with optional multi-threaded scanning.
- **Delete by extension** – Delete files matching one or more extensions.
- **Clean folder** – Delete files in a folder, optionally excluding certain names.
- **Delete empty folders** – Remove empty directories, optionally recursively.
- **Delete hidden files** – Remove hidden files (dot-files on POSIX, hidden
  attribute on Windows).
- **Compress files** – Bundle files from a directory into a timestamped ZIP
  archive, with optional extension and name filters.
- **Dry-run mode** – Preview any command without modifying the file system.
- **Configurable logging** – Log to a file at a chosen level (`DEBUG`, `INFO`,
  `WARNING`, ...).

## Requirements

- Python 3.10+ (uses `TypeAlias` and other modern typing features)
- Dependencies listed in [requirements.txt](requirements.txt)

## Installation

```bash
# Clone the repository
git clone https://github.com/neolace/file-manager.git
cd file-manager

# (Recommended) create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the tool via `main.py`, selecting an operation with `--command`:

```bash
python main.py --command <command> [options]
```

### Common options

These options apply to every command:

| Option        | Default   | Description                                              |
| ------------- | --------- | -------------------------------------------------------- |
| `--command`   | *(required)* | Command to execute (see below).                       |
| `--log`       | `app.log` | Path to the log file.                                    |
| `--log-level` | `INFO`    | Logging level (`DEBUG`, `INFO`, `WARNING`, ...).         |
| `--dry-run`   | `false`   | Simulate the action without modifying the file system.   |

## Commands

### `deduplicate`

Find duplicate files by content hash and remove the duplicates.

| Option          | Required | Description                                |
| --------------- | -------- | ------------------------------------------ |
| `--directory`   | Yes      | Target directory to scan (recursively).    |
| `--max-workers` | No       | Worker threads for hashing (default `1`).  |

```bash
python main.py --command deduplicate --directory ./photos --max-workers 4 --dry-run
```

### `delete_by_extension`

Delete files matching the given extensions.

| Option         | Required | Description                                          |
| -------------- | -------- | ---------------------------------------------------- |
| `--path`       | Yes      | Target directory.                                    |
| `--extensions` | Yes      | Comma-separated list of extensions (e.g. `tmp,log`). |

```bash
python main.py --command delete_by_extension --path ./downloads --extensions tmp,log
```

### `clean_folder`

Delete files within a folder, optionally excluding certain names.

| Option             | Required | Description                                       |
| ------------------ | -------- | ------------------------------------------------- |
| `--path`           | Yes      | Target directory.                                 |
| `--excluded-names` | No       | Comma-separated names to exclude from cleaning.   |

```bash
python main.py --command clean_folder --path ./tmp --excluded-names keep.txt,.gitkeep
```

### `delete_empty`

Delete empty folders, optionally recursively.

| Option        | Required | Description                                   |
| ------------- | -------- | --------------------------------------------- |
| `--path`      | Yes      | Target directory.                             |
| `--recursive` | No       | Recurse into subdirectories when set.         |

```bash
python main.py --command delete_empty --path ./project --recursive
```

### `delete_hidden_files`

Delete hidden files (dot-files on POSIX; hidden attribute on Windows).

| Option             | Required | Description                                     |
| ------------------ | -------- | ----------------------------------------------- |
| `--path`           | Yes      | Target directory.                               |
| `--excluded-names` | No       | Comma-separated names to exclude.               |

```bash
python main.py --command delete_hidden_files --path ./repo --dry-run
```

### `compress_files`

Compress files from a directory into a timestamped ZIP archive. The archive is
created in the parent directory as `<folder-name>_<YYYYMMDD_HHMMSS>.zip`.

| Option             | Required | Description                                                    |
| ------------------ | -------- | ------------------------------------------------------------- |
| `--path`           | Yes      | Directory whose files should be compressed.                  |
| `--extensions`     | No       | Comma-separated extensions to include (all files if omitted). |
| `--excluded-names` | No       | Comma-separated names to exclude.                            |

```bash
python main.py --command compress_files --path ./logs --extensions log,txt
```

> **Note:** The `move` command is registered but its execution is not yet
> implemented.

## Dry-run mode

Add `--dry-run` to any command to log exactly what would happen without deleting,
moving, or writing anything:

```bash
python main.py --command deduplicate --directory ./photos --dry-run
```

## Project structure

```text
main.py                       # Entry point: argument parsing, command dispatch, logging
requirements.txt              # Python dependencies
config/                       # Configuration and constants
  settings.py                 # Central Config (buffer sizes, messages, defaults)
  fm_FileType.py              # Supported file types
  LogLevel.py                 # Log level definitions
functions/                    # Command implementations
  CommandType.py              # Enum of supported commands
  CompressFilesCommand.py
  CleanFolderCommand.py
  DeleteByExtensionCommand.py
  DeleteEmptyFoldersCommand.py
  DeleteHiddenFilesCommand.py
  FileDeduplicator.py
  MoveCommand.py
  ProcessFilesCommandBase.py  # Shared base for file-processing commands
  exceptions.py               # Custom exception hierarchy
Interface/
  CommandInterface.py         # Command contract (validate/execute/description)
utils/                        # Helpers: argument parsing, validation, logging, filtering
```

## Architecture

- **`CommandInterface`** defines the contract every command implements:
  `validate(args)`, `execute(args, logger)`, and a `description` property.
- **`CommandRegistry`** maps command names to their implementations.
- **`CommandHandler`** looks up the command, validates arguments, executes it,
  and maps known exceptions to friendly log messages.
- **`ProcessFilesCommandBase`** provides shared file-walking logic for commands
  that operate on individual files.

### Adding a new command

1. Add a new value to `CommandType` in [functions/CommandType.py](functions/CommandType.py).
2. Implement a class that satisfies `CommandInterface` (or extend
   `ProcessFilesCommandBase`).
3. Register it in `CommandRegistry.COMMAND_MAP` in [main.py](main.py).
4. Add any new CLI arguments in [utils/parse_arguments.py](utils/parse_arguments.py).

## Testing

Tests use `pytest`:

```bash
pytest
# with coverage
pytest --cov
```

## Development

The project ships with common tooling in [requirements.txt](requirements.txt):

- Formatting: `black`, `isort`
- Linting: `flake8`, `pylint`
- Type checking: `mypy`
- Testing: `pytest`, `pytest-cov`

```bash
black .
isort .
flake8
mypy .
```
