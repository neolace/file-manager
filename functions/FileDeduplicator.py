import logging
import os
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from functions.exceptions import ArgumentError, DirectoryError, FileError, PathError
from Interface.CommandInterface import CommandInterface, CommandRequest, CommandResult
from Interface.FileSystemExecutor import (
    FileSystemExecutor,
    MutationRecord,
    calculate_file_digest,
)


@dataclass(frozen=True)
class DuplicateGroup:
    keeper: Path
    duplicates: Tuple[Path, ...]
    digest: str


@dataclass(frozen=True)
class DeduplicationPlan:
    total_files: int
    unique_files: int
    groups: Tuple[DuplicateGroup, ...]

    @property
    def duplicates_found(self) -> int:
        return sum(len(group.duplicates) for group in self.groups)


@dataclass(frozen=True, kw_only=True)
class DeduplicateRequest(CommandRequest):
    directory: Path
    max_workers: int


@dataclass(frozen=True, kw_only=True)
class DeduplicationResult(CommandResult):
    total_files: int
    unique_files: int
    duplicates_found: int
    plan: DeduplicationPlan


class DeduplicateCommand(CommandInterface[DeduplicateRequest, DeduplicationResult]):
    @property
    def description(self) -> str:
        return "Deduplicate files in a directory"

    def parse(
        self, args: Namespace, executor: FileSystemExecutor
    ) -> DeduplicateRequest:
        directory = getattr(args, "directory", None)
        if not directory:
            raise ArgumentError(f"'directory' is required for {self.description}")
        max_workers = getattr(args, "max_workers", 1)
        return DeduplicateRequest(
            executor=executor,
            directory=Path(directory),
            max_workers=max_workers,
        )

    def execute(
        self, request: DeduplicateRequest, logger: logging.Logger
    ) -> DeduplicationResult:
        self._validate(request)
        plan = self._build_plan(request)
        records: List[MutationRecord] = []
        errors: List[str] = []

        for group in plan.groups:
            logger.debug("Keeping duplicate-group file: %s", group.keeper)
            for duplicate in group.duplicates:
                try:
                    record = request.executor.delete_duplicate(
                        duplicate, group.keeper, group.digest
                    )
                    records.append(record)
                    action = "Removed" if record.applied else "Would remove"
                    logger.info("%s duplicate: %s", action, duplicate)
                except OSError as error:
                    message = f"{duplicate}: {error}"
                    errors.append(message)
                    logger.error("Failed to remove duplicate %s: %s", duplicate, error)

        return DeduplicationResult(
            attempted=plan.duplicates_found,
            succeeded=len(records),
            skipped=0,
            failed=len(errors),
            records=tuple(records),
            errors=tuple(errors),
            total_files=plan.total_files,
            unique_files=plan.unique_files,
            duplicates_found=plan.duplicates_found,
            plan=plan,
        )

    @staticmethod
    def _validate(request: DeduplicateRequest) -> None:
        if not request.directory.exists():
            raise PathError(f"Path not found: {request.directory}")
        if not request.directory.is_dir():
            raise DirectoryError(f"Path is not a directory: {request.directory}")
        if not isinstance(request.max_workers, int) or request.max_workers < 1:
            raise ArgumentError(
                f"'max_workers' must be a positive integer, got {request.max_workers}"
            )

    def _build_plan(self, request: DeduplicateRequest) -> DeduplicationPlan:
        files = sorted(
            (
                path
                for path in request.directory.rglob("*")
                if path.is_file() and not path.is_symlink()
            ),
            key=self._path_key,
        )
        files_by_hash: Dict[str, List[Path]] = {}
        with ThreadPoolExecutor(max_workers=request.max_workers) as executor:
            for path, digest in executor.map(self._hash_file, files):
                files_by_hash.setdefault(digest, []).append(path)

        groups = tuple(
            DuplicateGroup(
                keeper=paths[0],
                duplicates=tuple(paths[1:]),
                digest=digest,
            )
            for digest, paths in files_by_hash.items()
            if len(paths) > 1
        )
        return DeduplicationPlan(
            total_files=len(files),
            unique_files=len(files_by_hash),
            groups=groups,
        )

    @staticmethod
    def _path_key(path: Path) -> str:
        return os.path.normcase(str(path.resolve()))

    @staticmethod
    def _hash_file(path: Path) -> Tuple[Path, str]:
        try:
            digest = calculate_file_digest(path)
        except OSError as error:
            raise FileError(f"Failed to read {path}: {error}") from error
        return path, digest
