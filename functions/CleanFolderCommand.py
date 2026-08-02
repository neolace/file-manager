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


class CleanFolderCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Clean a folder by deleting files, with optional exclusions"

    def parse(
        self, args: Namespace, executor: FileSystemExecutor
    ) -> ProcessFilesRequest:
        path = getattr(args, "path", None)
        if not path:
            raise ArgumentError(f"'path' is required for {self.description}")
        excluded_names = parse_string_list(getattr(args, "excluded_names", None))
        return ProcessFilesRequest(
            executor=executor,
            path=Path(path),
            file_filter=FileFilter(excluded_names=excluded_names),
        )
