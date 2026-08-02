# File Manager

A command-line file management utility for common house-keeping tasks such as
deduplicating files, deleting files by extension, cleaning folders, removing
empty directories, deleting hidden files, and compressing files into a ZIP
archive.

The tool is built around typed Commands. Each Command converts CLI arguments to
an immutable request, validates before mutation, and returns a structured result.
The `--dry-run` mode records target-file mutations without applying them.

## Features

- **Deduplicate** – Find and remove duplicate files using SHA-256 content hashing,
  with optional multi-threaded scanning.
- **Delete by extension** – Delete files matching one or more extensions.
- **Clean folder** – Delete files in a folder, optionally excluding certain names.
- **Delete empty folders** – Remove empty directories, optionally recursively.
- **Delete hidden files** – Remove hidden files (dot-files on POSIX, hidden
  attribute on Windows).
- **Compress files** – Bundle files from a directory into a timestamped ZIP
  archive, with optional extension and name filters.
- **Dry-run mode** – Preview target-file mutations without applying them.
- **Configurable logging** – Log to a file at a chosen level (`DEBUG`, `INFO`,
  `WARNING`, ...).

## Requirements

- Python 3.10+ (uses modern union types and frozen dataclasses)
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

## Dry-run mode

Add `--dry-run` to record the target-file mutations that would be attempted
without applying them. Diagnostic logging may still write to the configured log
file:

```bash
python main.py --command deduplicate --directory ./photos --dry-run
```

## Project structure

```text
main.py                       # Entry point: argument parsing, command dispatch, logging
requirements.txt              # Python dependencies
functions/                    # Command implementations
  CompressFilesCommand.py
  CleanFolderCommand.py
  DeleteByExtensionCommand.py
  DeleteEmptyFoldersCommand.py
  DeleteHiddenFilesCommand.py
  FileDeduplicator.py
  ProcessFilesCommandBase.py  # Filtering, mutation, and outcome collection
  exceptions.py               # Custom exception hierarchy
Interface/
  CommandInterface.py         # Typed request/result Command interface
  FileSystemExecutor.py       # Real and recording mutation adapters
tests/                        # Command, executor, filtering, and handler tests
utils/                        # Argument parsing, logging, and filtering
```

## Architecture

- **`CommandInterface`** defines `parse(args, executor)`,
  `execute(request, logger) -> result`, and a `description` property.
- **`CommandRegistry`** maps command names to their implementations.
- **`CommandHandler`** selects the real or recording executor, builds a typed
  request, executes the Command, and maps its result to an exit code.
- **`FileSystemExecutor`** is the seam for semantic target-file mutations. Its
  real and recording adapters make dry-run use the same Command path.
- **`ProcessFilesCommandBase`** owns filtering, deletion, accurate counting,
  and failure aggregation for Commands that delete matching files.

### Adding a new command

1. Implement a class that satisfies `CommandInterface` (or extend
   `ProcessFilesCommandBase`).
2. Register it in `CommandRegistry.COMMAND_MAP` in [main.py](main.py).
3. Add any new CLI arguments in [utils/parse_arguments.py](utils/parse_arguments.py).
4. Test through the Command interface and both executor adapters as applicable.

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
