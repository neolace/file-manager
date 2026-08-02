from argparse import Namespace
from pathlib import Path

from functions.exceptions import ArgumentError
from functions.ProcessFilesCommandBase import (
    ProcessFilesCommandBase,
    ProcessFilesRequest,
    parse_string_list,
)
from Interface.FileSystemExecutor import FileSystemExecutor
from utils.file_filter import FileFilter


class DeleteByExtensionCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Delete files by specified extensions in a directory"

    def parse(
        self, args: Namespace, executor: FileSystemExecutor
    ) -> ProcessFilesRequest:
        path = getattr(args, "path", None)
        extensions = parse_string_list(getattr(args, "extensions", None))
        if not path:
            raise ArgumentError(f"'path' is required for {self.description}")
        if not extensions:
            raise ArgumentError(f"'extensions' is required for {self.description}")
        return ProcessFilesRequest(
            executor=executor,
            path=Path(path),
            file_filter=FileFilter(extensions=extensions),
        )
