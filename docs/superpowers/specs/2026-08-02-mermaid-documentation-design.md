# Mermaid Documentation Design

## Goal

Bring the repository documentation into sync with the current CLI and add
purposeful Mermaid diagrams that make navigation, execution, contribution, and
failure behavior easier to understand.

## Scope

This design covers five new documents under `docs/`:

- `docs/README.md`
- `docs/user-guide.md`
- `docs/contributing.md`
- `docs/troubleshooting.md`
- `docs/safety-model.md`

It also corrects stale claims in the existing `README.md`, `CONTEXT.md`, and
`docs/tasks.md`. The root README remains a concise landing page. `CONTEXT.md`
remains the canonical domain vocabulary required by the repository.

## Document Ownership

### Documentation Index

`docs/README.md` is the entry point for the documentation set. It explains which
document serves each audience and links to every current guide.

Its Mermaid flowchart routes:

- people running commands to `docs/user-guide.md`;
- people assessing mutation safety to `docs/safety-model.md`;
- people diagnosing failures to `docs/troubleshooting.md`;
- people changing code to `docs/contributing.md`;
- people reviewing architecture terminology to `CONTEXT.md`.

The diagram is navigational, not an architecture diagram. Link destinations are
also present as ordinary Markdown links so navigation does not depend on Mermaid
click support.

### User Guide

`docs/user-guide.md` is the sole detailed CLI and command reference. It owns:

- shared invocation and options;
- exact registered command names;
- required command arguments;
- recursive behavior;
- command-specific result units;
- dry-run behavior visible to users;
- exit statuses;
- one complete example for each command.

Its Mermaid flowchart shows the common command lifecycle:

1. Parse the shared CLI arguments.
2. Resolve the registered Command.
3. Select the real or recording executor.
4. Build and validate the immutable request.
5. Plan or select targets.
6. Record or apply semantic mutations.
7. Return a structured result.
8. Map the result to exit code `0` or `1`.

Argparse rejection is shown as a separate exit-code-`2` path before Command
execution.

Detailed filtering, symlink, partial-failure, deduplication revalidation, and
archive publication rules link to `docs/safety-model.md` rather than being
duplicated.

### Contributor and Testing Guide

`docs/contributing.md` owns local setup, architecture constraints, test design,
formatting, static checks, documentation ownership, and commit discipline.

Its Mermaid flowchart shows the expected change cycle:

1. Select the smallest behavior change.
2. Write a focused failing pytest test.
3. Confirm the expected failure.
4. Implement the smallest change.
5. Run the focused test.
6. Apply Black and isort.
7. Run pytest, Black check, isort check, flake8, and mypy.
8. Update the owning documentation.
9. Review and commit the independently testable change.

The diagram must not imply that CI or pre-commit hooks exist.

### Troubleshooting Guide

`docs/troubleshooting.md` owns user-visible diagnosis and recovery. It covers:

- argparse exit code `2`;
- command/result exit code `1`;
- missing and invalid paths;
- partial failures without rollback;
- deduplication revalidation failures;
- empty compression selections;
- archive timestamp collisions and no-overwrite publication;
- logging fallback behavior;
- hidden-file selection;
- symlink cautions.

Its Mermaid decision tree begins with the process exit status and then directs
the reader to CLI syntax, logs, per-target errors, deduplication revalidation,
archive publication, or successful empty-selection behavior. Recovery text stays
outside the chart so it remains searchable and accessible.

### Safety Model

`docs/safety-model.md` is the authoritative cross-cutting behavior reference. It
owns four related topics that otherwise become fragmented across command docs.

#### Filtering

A Mermaid flowchart documents the `FileFilter.matches()` pipeline in execution
order:

1. Candidate must resolve as a file through `Path.is_file()`.
2. Exact, case-sensitive excluded basenames reject the candidate.
3. Excluded extensions reject before included extensions are considered.
4. Included extensions use lowercased final suffixes with leading dots removed.
5. Inclusive minimum and maximum size bounds are checked.
6. Hidden-mode criteria are checked against the file itself.
7. Accepted files are sorted by normalized resolved path.

The surrounding text states that file-selection Commands recurse by default and
that hidden status is not inherited from parent directories.

#### Symlinks

A Mermaid flowchart branches by operation:

- deduplication excludes file symlinks;
- empty-directory deletion excludes directory symlinks;
- shared file filtering can select a file symlink when `Path.is_file()` follows
  it to a regular file;
- deletion unlinks a selected file symlink rather than its target;
- compression reads a selected member through the symlink.

The text recommends dry-run inspection for trees containing links and avoids
claiming a repository-wide symlink policy that the code does not implement.

#### Partial Failures

A Mermaid sequence diagram shows a Command iterating planned targets, the
executor succeeding for one target, raising `OSError` for another, the Command
recording that failure, continuing to later targets, and returning a failed
structured result. `CommandHandler` maps that result to exit code `1`.

The text explicitly states that earlier successful mutations remain applied and
are not rolled back.

#### Archive Publication

A Mermaid flowchart shows:

1. Select recursive members.
2. Return one skipped unit and create no archive when selection is empty.
3. Write a temporary ZIP beside the destination.
4. Store member names relative to the source.
5. Publish with `os.link` without overwriting an existing destination.
6. Remove temporary output in all completion paths.
7. Return one success or one failure for the archive operation.

The text states that timestamped names have one-second precision and collisions
preserve the existing destination.

## Existing Document Corrections

### README

The root `README.md` becomes a concise landing page. It retains installation,
quick-start examples, project structure, and a short architecture summary. It
links to the documentation index and guides instead of duplicating detailed
command, safety, testing, or troubleshooting content.

Its dry-run wording says target-file mutations are not applied while diagnostic
logging may still write to disk. Its hidden-file wording covers dot-prefixed
names on every supported platform plus the Windows hidden attribute.

### Domain Context

`CONTEXT.md` uses the exact underscore command identifiers from
`CommandRegistry.COMMAND_MAP`, names `CompressFilesRequest`, and narrows its
normalization claim to Command-owned parsing and normalization.

The `DeduplicationPlan` definition states that planning precedes mutation, file
symlinks are excluded, the keeper is deterministic, and both keeper and duplicate
are revalidated against the planned digest immediately before unlinking. It links
to `docs/safety-model.md` for operational detail.

### Task Tracker

`docs/tasks.md` removes deleted implementation identifiers and narrows completed
claims about error handling, filtering, validation, fixtures, and coverage. A
documentation item is marked complete only in the same task that creates its
document.

## Mermaid Conventions

- Use fenced `mermaid` blocks supported by GitHub Markdown.
- Prefer `flowchart TD` for navigation and decision flows.
- Use one `sequenceDiagram` only for partial-failure aggregation.
- Keep node identifiers ASCII and labels short enough to scan without horizontal
  scrolling.
- Put exact command names, paths, flags, and error wording in prose or tables;
  diagrams summarize flow rather than replace reference text.
- Do not use Mermaid click directives, custom themes, initialization blocks, or
  external assets.
- Every diagram has an introductory sentence and complete adjacent prose so the
  document remains usable when Mermaid is not rendered.

## Validation

Implementation must verify:

- every registered command appears in the user guide;
- every new document exists under `docs/`;
- all ordinary Markdown links resolve;
- each new document contains at least one Mermaid block;
- `docs/safety-model.md` contains four Mermaid blocks, including one
  `sequenceDiagram`;
- Mermaid fences are balanced and each block begins with an approved diagram
  declaration;
- the exact recursive Commands and safety invariants appear in prose;
- the current pytest suite remains green;
- Black, isort, flake8, and mypy checks remain green.

No Mermaid CLI dependency is added. Validation checks document structure and
required diagram declarations; GitHub remains the target renderer.

## Deliberate Omissions

- No Sphinx API site is added for the un-packaged CLI.
- No changelog or release policy is invented without an existing versioning
  process.
- No separate examples directory duplicates command examples from the user guide.
- No executable behavior changes are included in this documentation project.
- Existing `README.md` and `CONTEXT.md` are not moved; all newly created documents
  remain under `docs/`.

## Acceptance Criteria

- A new user can identify the recursive scope and dry-run limitations before
  running a destructive Command.
- A contributor can find the exact architecture constraints and required local
  checks without consulting private instructions.
- A user can diagnose exit codes, partial failures, deduplication revalidation,
  logging fallback, and archive collisions from one troubleshooting guide.
- Filtering, symlink, partial-failure, and archive publication behavior has one
  cohesive source of truth.
- Every new guide contains a purposeful Mermaid diagram, while the safety model
  contains the four diagrams needed for its distinct behaviors.
- Detailed facts are not duplicated between the root README, user guide, safety
  model, contributor guide, and troubleshooting guide.
