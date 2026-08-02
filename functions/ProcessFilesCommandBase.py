import logging
from abc import abstractmethod
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Tuple

from functions.exceptions import DirectoryError, PathError
from Interface.CommandInterface import CommandInterface, CommandRequest, CommandResult
from Interface.FileSystemExecutor import FileSystemExecutor
from utils.file_filter import FileFilter


def parse_string_list(value: Optional[str | Sequence[str]]) -> Tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return tuple(item.strip() for item in value.split(",") if item.strip())
    return tuple(value)


@dataclass(frozen=True, kw_only=True)
class ProcessFilesRequest(CommandRequest):
    path: Path
    file_filter: FileFilter


@dataclass(frozen=True, kw_only=True)
class ProcessedFilesResult(CommandResult):
    pass


class ProcessFilesCommandBase(
    CommandInterface[ProcessFilesRequest, ProcessedFilesResult]
):
    @abstractmethod
    def parse(
        self, args: Namespace, executor: FileSystemExecutor
    ) -> ProcessFilesRequest:
        pass

    def execute(
        self, request: ProcessFilesRequest, logger: logging.Logger
    ) -> ProcessedFilesResult:
        self._validate(request.path)
        files = request.file_filter.filter_files(request.path)
        records = []
        errors = []

        for file_path in files:
            try:
                record = request.executor.delete_file(file_path)
                records.append(record)
                action = "Deleted" if record.applied else "Would delete"
                logger.info("%s: %s", action, file_path)
            except OSError as error:
                message = f"{file_path}: {error}"
                errors.append(message)
                logger.error("Failed to delete %s: %s", file_path, error)

        result = ProcessedFilesResult(
            attempted=len(files),
            succeeded=len(records),
            skipped=0,
            failed=len(errors),
            records=tuple(records),
            errors=tuple(errors),
        )
        logger.info(
            "%s finished: %d succeeded, %d failed",
            self.description,
            result.succeeded,
            result.failed,
        )
        return result

    @staticmethod
    def _validate(path: Path) -> None:
        if not path.exists():
            raise PathError(f"Path not found: {path}")
        if not path.is_dir():
            raise DirectoryError(f"Path is not a directory: {path}")
