# Safety Model

This document is the source of truth for behavior shared by multiple Commands:
file filtering, symlink treatment, partial failures, deduplication revalidation,
and archive publication. See the [user guide](user-guide.md) for command syntax.

Dry-run replaces the real mutation executor with a recording executor. It still
validates paths, traverses directories, reads metadata, and hashes file contents
for deduplication. Diagnostic logging may create or append to the configured log
file.

## File Selection

`delete_by_extension`, `clean_folder`, `delete_hidden_files`, and
`compress_files` use the immutable `FileFilter`. They call `filter_files()` with
its default `recursive=True`, so candidates at every depth are considered.

The matching pipeline is evaluated in this order:

```mermaid
flowchart TD
    Candidate["Candidate path"] --> IsFile{"Path.is_file()?"}
    IsFile -->|No| Reject["Reject candidate"]
    IsFile -->|Yes| Name{"Exact basename excluded?"}
    Name -->|Yes| Reject
    Name -->|No| ExcludedExt{"Final suffix excluded?"}
    ExcludedExt -->|Yes| Reject
    ExcludedExt -->|No| IncludedExt{"Included suffix required and absent?"}
    IncludedExt -->|Yes| Reject
    IncludedExt -->|No| Size{"Within inclusive size bounds?"}
    Size -->|No| Reject
    Size -->|Yes| Hidden{"Matches hidden mode?"}
    Hidden -->|No| Reject
    Hidden -->|Yes| Accept["Accept candidate"]
    Accept --> Sort["Sort accepted paths by normalized resolved path"]
```

Extension criteria are case-insensitive and may include a leading dot. Matching
uses only `Path.suffix`, so `archive.tar.gz` has extension `gz`. Excluded
extensions take precedence over included extensions. Excluded names are exact,
case-sensitive basenames.

Minimum and maximum sizes are inclusive. Hidden mode checks the file itself: a
dot-prefixed basename is hidden on every supported platform, and the Windows
hidden attribute is an additional criterion on Windows. Hidden status is not
inherited from parent directories.

## Symlink Treatment

The repository has operation-specific symlink behavior rather than one universal
policy:

```mermaid
flowchart TD
    Operation{"Which operation?"}
    Operation -->|deduplicate| NoFileLinks["Exclude file symlinks"]
    Operation -->|delete_empty| NoDirectoryLinks["Exclude directory symlinks"]
    Operation -->|shared FileFilter| Resolves{"Path.is_file()?"}
    Resolves -->|No| Ignore["Ignore candidate"]
    Resolves -->|Yes| Selected["Select file symlink"]
    Selected --> Action{"Selected action"}
    Action -->|delete| Unlink["Unlink the symlink"]
    Action -->|compress| Read["Read member through the symlink"]
```

Deduplication explicitly excludes file symlinks before hashing. Empty-directory
planning excludes directory symlinks. The shared filter uses `Path.is_file()`,
which can follow a file symlink to determine that it resolves to a regular file.
Deleting that selected path unlinks the symlink, not its target; compression
reads the member through the symlink.

Use dry-run and inspect the selected paths before operating on a tree containing
links.

## Partial Failures and Deduplication Revalidation

File deletion, empty-directory deletion, and deduplication aggregate supported
per-target `OSError` failures. They retain successful mutation records, record
the failed target, and continue with later planned targets:

```mermaid
sequenceDiagram
    participant P as Process
    participant H as CommandHandler
    participant C as Command
    participant E as FileSystemExecutor
    P->>H: Execute parsed command
    H->>C: Execute immutable request
    C->>E: Apply target A
    E-->>C: MutationRecord applied
    C->>E: Apply target B
    E-->>C: Raise OSError
    Note over C: Record failure and continue
    C->>E: Apply target C
    E-->>C: MutationRecord applied
    C-->>H: CommandResult with failed work
    H-->>P: Exit code 1
```

There is no rollback. If target A changed successfully before target B failed,
target A remains changed. Dry-run records planned mutations as succeeded work
with `MutationRecord.applied=False`; this reports that the intent was recorded,
not that a target was changed.

Deduplication builds its complete `DeduplicationPlan` before requesting any
deletion. It excludes file symlinks and keeps the lexicographically smallest
normalized absolute path in each SHA-256 digest group. Immediately before
unlinking a duplicate, the real executor:

1. captures the duplicate and keeper file state;
2. rehashes both files against the planned digest;
3. checks that neither observed file state changed during revalidation;
4. unlinks the duplicate only after those checks pass.

A failed digest or file-state check raises `MutationPreconditionError`, which is
an `OSError`; deduplication records that duplicate as failed, leaves it in place,
and continues. These checks reduce the stale-plan window but cannot make separate
filesystem reads and unlinking atomic.

Compression differs because one archive is one operation. It converts an
ordinary archive-creation exception into one failed result rather than
aggregating member-level failures.

## Archive Publication

Compression recursively selects members, writes a temporary archive, and
publishes without replacing an existing destination:

```mermaid
flowchart TD
    Select["Recursively select members"] --> Empty{"Selection empty?"}
    Empty -->|Yes| Skip["Return one skipped unit; create no archive"]
    Empty -->|No| Temporary["Create temporary file beside destination"]
    Temporary --> Write["Write ZIP with source-relative member names"]
    Write --> Publish["Publish with os.link"]
    Publish --> Exists{"Destination already exists or publication fails?"}
    Exists -->|No| Success["Return one successful archive unit"]
    Exists -->|Yes| Failure["Keep existing destination; return one failure"]
    Success --> Cleanup["Remove temporary file"]
    Failure --> Cleanup
```

The destination is `<source-name>_<YYYYMMDD_HHMMSS>.zip` in the source
directory's parent. Names have one-second precision. `os.link` refuses to
overwrite an existing or concurrently created destination, and publication
requires hard-link support in the destination filesystem.

Archive members use paths relative to the source directory. Temporary output is
removed in a `finally` block after success, ordinary failure, or a process-control
exception. A non-empty selection counts as one attempted archive regardless of
member count.
