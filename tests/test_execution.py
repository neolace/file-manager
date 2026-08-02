import logging
import zipfile
from argparse import Namespace
from dataclasses import FrozenInstanceError, dataclass
from pathlib import Path

import pytest

import Interface.FileSystemExecutor as executor_module
from Interface.CommandInterface import CommandInterface, CommandRequest, CommandResult
from Interface.FileSystemExecutor import (
    FileSystemExecutor,
    MutationAction,
    RealFileSystemExecutor,
    RecordingFileSystemExecutor,
)


@dataclass(frozen=True, kw_only=True)
class ExampleRequest(CommandRequest):
    value: int


class ExampleCommand(CommandInterface[ExampleRequest, CommandResult]):
    @property
    def description(self) -> str:
        return "Example"

    def parse(self, args: Namespace, executor: FileSystemExecutor) -> ExampleRequest:
        return ExampleRequest(executor=executor, value=args.value)

    def execute(self, request: ExampleRequest, logger: logging.Logger) -> CommandResult:
        return CommandResult(
            attempted=1,
            succeeded=1,
            skipped=0,
            failed=0,
            records=(),
            errors=(),
        )


def test_command_request_is_immutable() -> None:
    request = ExampleRequest(executor=RecordingFileSystemExecutor(), value=1)

    with pytest.raises(FrozenInstanceError):
        request.value = 2  # type: ignore[misc]


def test_command_interface_returns_a_typed_result() -> None:
    executor = RecordingFileSystemExecutor()
    command = ExampleCommand()
    request = command.parse(Namespace(value=7), executor)

    result = command.execute(request, logging.getLogger("test"))

    assert request.value == 7
    assert result.succeeded == 1
    assert result.ok


def test_recording_executor_records_delete_without_mutating(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("keep me", encoding="utf-8")
    executor = RecordingFileSystemExecutor()

    record = executor.delete_file(target)

    assert target.exists()
    assert record.action is MutationAction.DELETE_FILE
    assert record.source == target
    assert not record.applied
    assert executor.records == (record,)


def test_real_executor_applies_semantic_mutations(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("delete me", encoding="utf-8")
    empty_directory = tmp_path / "empty"
    empty_directory.mkdir()
    archive_source = tmp_path / "source"
    archive_source.mkdir()
    archive_member = archive_source / "member.txt"
    archive_member.write_text("archive me", encoding="utf-8")
    archive_path = tmp_path / "archive.zip"
    executor = RealFileSystemExecutor()

    delete_record = executor.delete_file(target)
    directory_record = executor.delete_empty_directory(empty_directory)
    archive_record = executor.create_archive(
        archive_source, archive_path, (archive_member,)
    )

    assert not target.exists()
    assert not empty_directory.exists()
    assert delete_record.applied
    assert directory_record.applied
    assert archive_record.applied
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.namelist() == ["member.txt"]


def test_archive_creation_never_overwrites_an_existing_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    member = source / "member.txt"
    member.write_text("member", encoding="utf-8")
    destination = tmp_path / "archive.zip"
    destination.write_bytes(b"existing archive")

    with pytest.raises(FileExistsError):
        RealFileSystemExecutor().create_archive(source, destination, (member,))

    assert destination.read_bytes() == b"existing archive"


def test_failed_archive_creation_removes_partial_output(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    member = source / "member.txt"
    member.write_text("member", encoding="utf-8")
    missing_member = source / "missing.txt"
    destination = tmp_path / "archive.zip"

    with pytest.raises(FileNotFoundError):
        RealFileSystemExecutor().create_archive(
            source, destination, (member, missing_member)
        )

    assert not destination.exists()


def test_archive_publication_does_not_overwrite_a_concurrent_file(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    member = source / "member.txt"
    member.write_text("member", encoding="utf-8")
    destination = tmp_path / "archive.zip"
    original_link = executor_module.os.link

    def race_with_publication(source_path: Path, destination_path: Path) -> None:
        Path(destination_path).write_bytes(b"concurrent file")
        original_link(source_path, destination_path)

    monkeypatch.setattr(executor_module.os, "link", race_with_publication)

    with pytest.raises(FileExistsError):
        RealFileSystemExecutor().create_archive(source, destination, (member,))

    assert destination.read_bytes() == b"concurrent file"


def test_archive_cleanup_runs_for_process_control_exceptions(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    member = source / "member.txt"
    member.write_text("member", encoding="utf-8")
    destination = tmp_path / "archive.zip"

    def interrupt_write(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise KeyboardInterrupt

    monkeypatch.setattr(zipfile.ZipFile, "write", interrupt_write)

    with pytest.raises(KeyboardInterrupt):
        RealFileSystemExecutor().create_archive(source, destination, (member,))

    assert not destination.exists()
    assert tuple(tmp_path.glob(".archive.zip.*.tmp")) == ()
