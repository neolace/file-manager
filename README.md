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
- **Delete hidden files** - Remove dot-prefixed files on every supported platform
  and files with the Windows hidden attribute.
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

## Quick Start

Run the tool through its only executable entrypoint, `main.py`:

```powershell
python main.py --command deduplicate --directory ./photos --dry-run
python main.py --command delete_by_extension --path ./downloads --extensions tmp,log --dry-run
python main.py --command clean_folder --path ./tmp --excluded-names keep.txt --dry-run
python main.py --command delete_empty --path ./project --recursive --dry-run
python main.py --command delete_hidden_files --path ./repo --dry-run
python main.py --command compress_files --path ./logs --extensions log,txt --dry-run
```

Start destructive operations with `--dry-run`. It records target-file mutations
without applying them, although diagnostic logging may still create or append to
the configured log file.

See the [user guide](docs/user-guide.md) for required arguments, recursive
behavior, examples, and exit statuses. See the
[safety model](docs/safety-model.md) for filtering, symlinks, partial failures,
deduplication revalidation, and archive publication.

## Documentation

- [Documentation index](docs/README.md)
- [User guide](docs/user-guide.md)
- [Contributing](docs/contributing.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Safety model](docs/safety-model.md)
- [Domain and architecture vocabulary](CONTEXT.md)
- [Improvement tasks](docs/tasks.md)

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
4. Follow the test and documentation checklist in
   [docs/contributing.md](docs/contributing.md).

## Contributing

See [docs/contributing.md](docs/contributing.md) for environment setup,
architecture constraints, test design, formatting, and all required local checks.
