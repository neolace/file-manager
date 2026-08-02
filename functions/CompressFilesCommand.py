import logging
from argparse import Namespace
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

from functions.exceptions import ArgumentError, DirectoryError, PathError
from functions.ProcessFilesCommandBase import parse_string_list
from Interface.CommandInterface import CommandInterface, CommandRequest, CommandResult
from Interface.FileSystemExecutor import FileSystemExecutor
from utils.file_filter import FileFilter


@dataclass(frozen=True, kw_only=True)
class CompressFilesRequest(CommandRequest):
    path: Path
    archive_path: Path
    file_filter: FileFilter


@dataclass(frozen=True, kw_only=True)
class CompressionResult(CommandResult):
    archive_path: Path
    members: Tuple[Path, ...]


class CompressFilesCommand(CommandInterface[CompressFilesRequest, CompressionResult]):
    @property
    def description(self) -> str:
        return "Compress files in a directory into a single archive"

    def parse(
        self, args: Namespace, executor: FileSystemExecutor
    ) -> CompressFilesRequest:
        path_value = getattr(args, "path", None)
        if not path_value:
            raise ArgumentError(f"'path' is required for {self.description}")
        path = Path(path_value).resolve()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = path.parent / f"{path.name}_{timestamp}.zip"
        return CompressFilesRequest(
            executor=executor,
            path=path,
            archive_path=archive_path,
            file_filter=FileFilter(
                extensions=parse_string_list(getattr(args, "extensions", None)),
                excluded_names=parse_string_list(getattr(args, "excluded_names", None)),
            ),
        )

    def execute(
        self, request: CompressFilesRequest, logger: logging.Logger
    ) -> CompressionResult:
        self._validate(request.path)
        members = tuple(request.file_filter.filter_files(request.path))
        if not members:
            logger.warning("No files found to compress in %s", request.path)
            return CompressionResult(
                attempted=0,
                succeeded=0,
                skipped=1,
                failed=0,
                records=(),
                errors=(),
                archive_path=request.archive_path,
                members=(),
            )

        try:
            record = request.executor.create_archive(
                request.path, request.archive_path, members
            )
        except Exception as error:
            logger.error("Failed to create archive %s: %s", request.archive_path, error)
            return CompressionResult(
                attempted=1,
                succeeded=0,
                skipped=0,
                failed=1,
                records=(),
                errors=(f"{request.archive_path}: {error}",),
                archive_path=request.archive_path,
                members=members,
            )

        action = "Created" if record.applied else "Would create"
        logger.info("%s archive: %s", action, request.archive_path)
        return CompressionResult(
            attempted=1,
            succeeded=1,
            skipped=0,
            failed=0,
            records=(record,),
            errors=(),
            archive_path=request.archive_path,
            members=members,
        )

    @staticmethod
    def _validate(path: Path) -> None:
        if not path.exists():
            raise PathError(f"Path not found: {path}")
        if not path.is_dir():
            raise DirectoryError(f"Path is not a directory: {path}")
