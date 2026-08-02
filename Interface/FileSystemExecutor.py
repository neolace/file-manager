import hashlib
import os
import tempfile
import zipfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


class MutationAction(Enum):
    DELETE_FILE = auto()
    DELETE_DUPLICATE = auto()
    DELETE_EMPTY_DIRECTORY = auto()
    CREATE_ARCHIVE = auto()


@dataclass(frozen=True)
class MutationRecord:
    action: MutationAction
    source: Path
    destination: Optional[Path] = None
    members: Tuple[Path, ...] = ()
    expected_digest: Optional[str] = None
    applied: bool = False


class MutationPreconditionError(OSError):
    pass


def calculate_file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(65_536):
            digest.update(chunk)
    return digest.hexdigest()


def file_state(path: Path) -> Tuple[int, int, int, int, int]:
    state = path.stat()
    return (
        state.st_dev,
        state.st_ino,
        state.st_size,
        state.st_mtime_ns,
        state.st_ctime_ns,
    )


class FileSystemExecutor(ABC):
    @abstractmethod
    def delete_file(self, path: Path) -> MutationRecord:
        pass

    @abstractmethod
    def delete_duplicate(
        self, path: Path, keeper: Path, expected_digest: str
    ) -> MutationRecord:
        pass

    @abstractmethod
    def delete_empty_directory(self, path: Path) -> MutationRecord:
        pass

    @abstractmethod
    def create_archive(
        self, source: Path, destination: Path, members: Sequence[Path]
    ) -> MutationRecord:
        pass


class RealFileSystemExecutor(FileSystemExecutor):
    def delete_file(self, path: Path) -> MutationRecord:
        path.unlink()
        return MutationRecord(
            action=MutationAction.DELETE_FILE,
            source=path,
            applied=True,
        )

    def delete_duplicate(
        self, path: Path, keeper: Path, expected_digest: str
    ) -> MutationRecord:
        duplicate_state = file_state(path)
        keeper_state = file_state(keeper)
        if calculate_file_digest(path) != expected_digest:
            raise MutationPreconditionError(f"Duplicate changed after planning: {path}")
        if calculate_file_digest(keeper) != expected_digest:
            raise MutationPreconditionError(f"Keeper changed after planning: {keeper}")
        if file_state(path) != duplicate_state:
            raise MutationPreconditionError(
                f"Duplicate changed during deletion: {path}"
            )
        if file_state(keeper) != keeper_state:
            raise MutationPreconditionError(f"Keeper changed during deletion: {keeper}")
        path.unlink()
        return MutationRecord(
            action=MutationAction.DELETE_DUPLICATE,
            source=path,
            destination=keeper,
            expected_digest=expected_digest,
            applied=True,
        )

    def delete_empty_directory(self, path: Path) -> MutationRecord:
        path.rmdir()
        return MutationRecord(
            action=MutationAction.DELETE_EMPTY_DIRECTORY,
            source=path,
            applied=True,
        )

    def create_archive(
        self, source: Path, destination: Path, members: Sequence[Path]
    ) -> MutationRecord:
        member_tuple = tuple(members)
        temporary_path: Optional[Path] = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=destination.parent,
                prefix=f".{destination.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
            with zipfile.ZipFile(temporary_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for member in member_tuple:
                    archive.write(member, member.relative_to(source))
            os.link(temporary_path, destination)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
        return MutationRecord(
            action=MutationAction.CREATE_ARCHIVE,
            source=source,
            destination=destination,
            members=member_tuple,
            applied=True,
        )


class RecordingFileSystemExecutor(FileSystemExecutor):
    def __init__(self) -> None:
        self._records: List[MutationRecord] = []

    @property
    def records(self) -> Tuple[MutationRecord, ...]:
        return tuple(self._records)

    def _record(self, record: MutationRecord) -> MutationRecord:
        self._records.append(record)
        return record

    def delete_file(self, path: Path) -> MutationRecord:
        return self._record(
            MutationRecord(action=MutationAction.DELETE_FILE, source=path)
        )

    def delete_duplicate(
        self, path: Path, keeper: Path, expected_digest: str
    ) -> MutationRecord:
        return self._record(
            MutationRecord(
                action=MutationAction.DELETE_DUPLICATE,
                source=path,
                destination=keeper,
                expected_digest=expected_digest,
            )
        )

    def delete_empty_directory(self, path: Path) -> MutationRecord:
        return self._record(
            MutationRecord(
                action=MutationAction.DELETE_EMPTY_DIRECTORY,
                source=path,
            )
        )

    def create_archive(
        self, source: Path, destination: Path, members: Sequence[Path]
    ) -> MutationRecord:
        return self._record(
            MutationRecord(
                action=MutationAction.CREATE_ARCHIVE,
                source=source,
                destination=destination,
                members=tuple(members),
            )
        )
