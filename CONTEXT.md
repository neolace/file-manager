# Domain Context — File Manager

This file is the canonical vocabulary for the File Manager project.
Architecture reviews, grilling sessions, and ADRs use these terms exactly.

---

## Domain Terms

### Command
A self-contained file-system operation (`deduplicate`, `delete_by_extension`,
`clean_folder`, `delete_empty`, `delete_hidden_files`, or `compress_files`).
Every Command implements `CommandInterface`: `parse(args, executor)`,
`execute(request, logger)`, and a `description` property. Execution returns a
`CommandResult`.

### CommandRegistry
Maps lowercase command-name strings to their `Command` classes.
Lives in `main.py`. The single place to register a new Command.

### CommandHandler
Resolves a Command from `CommandRegistry`, selects a `FileSystemExecutor`,
builds a `CommandRequest`, calls `execute`, and maps known exception types and
the `CommandResult` to structured log output.
Returns an exit code (0 = success, 1 = error).

### FileFilter
Filters a directory tree to a list of matching `Path` objects.
Criteria: included extensions, excluded extensions, excluded names,
min/max size, and hidden status.
Lives in `utils/file_filter.py`.

### hidden file
A file whose own name follows the POSIX dot-prefix convention or whose own
Windows attributes mark it hidden. Hidden status is not inherited from a parent
directory; deleting hidden directory trees is a distinct operation.

### ProcessFilesCommandBase
An abstract `Command` base that owns filtering, deletion, accurate counting,
and failure aggregation. Subclasses only build the `FileFilter` needed by one
file-deletion Command.

### dry-run
A cross-cutting execution mode (`--dry-run` flag) in which every
target-domain mutation is planned and reported but not applied. Diagnostic
logging may still write to the configured log file.
The flag selects a recording `FileSystemExecutor`; Commands do not retain a
second execution-mode field.

### FileSystemExecutor
A seam between Command logic and target-file mutations.
Two adapters consume semantic mutation intents: a real executor applies them,
while a recording executor records them without changing target files. It does
not mirror every low-level filesystem function.

---

## Architectural Terms

### CommandRequest
A typed, immutable parameter object produced by a Command from command-line
arguments. Values required by a Command are parsed into their request before
execution; each Command owns any value-specific normalization it needs.
Every CommandRequest includes the selected `FileSystemExecutor`; specialised
requests add the inputs required by one Command, e.g. `DeduplicateRequest` or
`CompressFilesRequest`. The `--dry-run` flag selects the executor but is not
retained as a second execution-mode field.

### CommandResult
A typed outcome returned by a Command. It reports attempted, succeeded, skipped,
and failed work, with specialised results adding Command-specific facts.

### DeduplicationPlan
The deterministic classification of matching-content files into keepers and
duplicates before any duplicate is removed. File symlinks are excluded. The
lexicographically smallest normalized absolute path is the keeper when no
explicit keeper policy exists. Immediately before unlinking a duplicate, the
real executor revalidates the duplicate and keeper against the planned SHA-256
digest and verifies that their observed file state did not change during that
revalidation.

Filtering, symlink, partial-failure, revalidation, and archive-publication details
are documented in the [safety model](docs/safety-model.md).

---

## Glossary Notes

- **Seam** — a place in the code where behaviour can be swapped without
  editing that place (Feathers). The `CommandInterface` is the primary
  external seam; `FileFilter` is an internal seam used by several Commands.
- **Adapter** — a concrete implementation that satisfies an interface at a
  seam. `DeduplicateCommand`, `CompressFilesCommand`, etc. are adapters of
  `CommandInterface`.
- **depth** — leverage at the interface: more behaviour per unit of
  interface a caller must learn.
