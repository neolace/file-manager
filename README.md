# File Manager

A versatile file management utility that supports both Python and TypeScript/Node.js implementations for organizing
files by their extensions.

## Features

- Move or copy files by extension
- Recursive file search support
- Dry run capability (preview mode)
- Duplicate file handling
- Configurable source and destination folders
- Logging support

## Python Usage

```python
from pathlib import Path
from functions.move_files_by_extension import move_files_by_extension

# Move all PDF files from source to target
source = Path("./input")
target = Path("./output")
move_files_by_extension(source, target, "pdf")

# Dry run to preview changes
move_files_by_extension(source, target, "pdf", dry_run=True)
```

# Python dependencies

pip install -r requirements.txt
