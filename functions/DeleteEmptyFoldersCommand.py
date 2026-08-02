import logging
import os
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Tuple

from functions.exceptions import ArgumentError, DirectoryError, PathError
from Interface.CommandInterface import CommandInterface, CommandRequest, CommandResult
from Interface.FileSystemExecutor import FileSystemExecutor, MutationRecord


@dataclass(frozen=True, kw_only=True)
class DeleteEmptyFoldersRequest(CommandRequest):
    path: Path
    recursive: bool


@dataclass(frozen=True, kw_only=True)
class DeleteEmptyFoldersResult(CommandResult):
    planned_directories: Tuple[Path, ...]


class DeleteEmptyFoldersCommand(
    CommandInterface[DeleteEmptyFoldersRequest, DeleteEmptyFoldersResult]
):
    @property
    def description(self) -> str:
        return "Delete empty folders, optionally recursively"

    def parse(
        self, args: Namespace, executor: FileSystemExecutor
    ) -> DeleteEmptyFoldersRequest:
        path = getattr(args, "path", None)
        if not path:
            raise ArgumentError(f"'path' is required for {self.description}")
        return DeleteEmptyFoldersRequest(
            executor=executor,
            path=Path(path),
            recursive=bool(getattr(args, "recursive", False)),
        )

    def execute(
        self, request: DeleteEmptyFoldersRequest, logger: logging.Logger
    ) -> DeleteEmptyFoldersResult:
        self._validate(request.path)
        plan = self._plan(request.path, request.recursive)
        records: List[MutationRecord] = []
        errors: List[str] = []

        for directory in plan:
            try:
                record = request.executor.delete_empty_directory(directory)
                records.append(record)
                action = "Deleted" if record.applied else "Would delete"
                logger.info("%s empty folder: %s", action, directory)
            except OSError as error:
                message = f"{directory}: {error}"
                errors.append(message)
                logger.error("Failed to delete empty folder %s: %s", directory, error)

        return DeleteEmptyFoldersResult(
            attempted=len(plan),
            succeeded=len(records),
            skipped=0,
            failed=len(errors),
            records=tuple(records),
            errors=tuple(errors),
            planned_directories=plan,
        )

    @staticmethod
    def _validate(path: Path) -> None:
        if not path.exists():
            raise PathError(f"Path not found: {path}")
        if not path.is_dir():
            raise DirectoryError(f"Path is not a directory: {path}")

    @classmethod
    def _plan(cls, root: Path, recursive: bool) -> Tuple[Path, ...]:
        if not recursive:
            return tuple(
                sorted(
                    (
                        path
                        for path in root.iterdir()
                        if path.is_dir()
                        and not path.is_symlink()
                        and not any(path.iterdir())
                    ),
                    key=cls._path_key,
                )
            )

        candidates = sorted(
            (
                path
                for path in root.rglob("*")
                if path.is_dir() and not path.is_symlink()
            ),
            key=lambda path: (-len(path.parts), cls._path_key(path)),
        )
        planned: List[Path] = []
        planned_set: Set[Path] = set()
        for directory in candidates:
            entries = tuple(directory.iterdir())
            if all(entry.is_dir() and entry in planned_set for entry in entries):
                planned.append(directory)
                planned_set.add(directory)
        return tuple(planned)

    @staticmethod
    def _path_key(path: Path) -> str:
        return os.path.normcase(str(path.resolve()))
