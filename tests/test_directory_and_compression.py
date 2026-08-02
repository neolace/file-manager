import logging
from argparse import Namespace
from pathlib import Path
from typing import Sequence

import pytest

from functions.CompressFilesCommand import CompressFilesCommand
from functions.DeleteEmptyFoldersCommand import DeleteEmptyFoldersCommand
from Interface.FileSystemExecutor import (
    MutationRecord,
    RealFileSystemExecutor,
    RecordingFileSystemExecutor,
)

LOGGER = logging.getLogger("test.directory_and_compression")


def _nested_empty_directories(root: Path) -> tuple[Path, Path]:
    parent = root / "parent"
    child = parent / "child"
    child.mkdir(parents=True)
    return parent, child


def test_dry_run_records_the_full_empty_directory_cascade(
    tmp_path: Path,
) -> None:
    parent, child = _nested_empty_directories(tmp_path)
    executor = RecordingFileSystemExecutor()
    command = DeleteEmptyFoldersCommand()
    request = command.parse(Namespace(path=str(tmp_path), recursive=True), executor)

    result = command.execute(request, LOGGER)

    assert result.planned_directories == (child, parent)
    assert tuple(record.source for record in executor.records) == (child, parent)
    assert child.exists()
    assert parent.exists()
    assert tmp_path.exists()


def test_real_execution_consumes_the_same_empty_directory_plan(
    tmp_path: Path,
) -> None:
    parent, child = _nested_empty_directories(tmp_path)
    command = DeleteEmptyFoldersCommand()
    request = command.parse(
        Namespace(path=str(tmp_path), recursive=True),
        RealFileSystemExecutor(),
    )

    result = command.execute(request, LOGGER)

    assert result.planned_directories == (child, parent)
    assert result.succeeded == 2
    assert not child.exists()
    assert not parent.exists()
    assert tmp_path.exists()


def test_non_recursive_empty_deletion_only_plans_direct_children(
    tmp_path: Path,
) -> None:
    direct_empty = tmp_path / "direct-empty"
    direct_empty.mkdir()
    non_empty = tmp_path / "non-empty"
    nested_empty = non_empty / "nested-empty"
    nested_empty.mkdir(parents=True)
    executor = RecordingFileSystemExecutor()
    command = DeleteEmptyFoldersCommand()
    request = command.parse(Namespace(path=str(tmp_path), recursive=False), executor)

    result = command.execute(request, LOGGER)

    assert result.planned_directories == (direct_empty,)


def test_compression_records_one_complete_archive_intent(
    tmp_path: Path,
) -> None:
    text_file = tmp_path / "notes.txt"
    image_file = tmp_path / "image.jpg"
    text_file.write_text("text", encoding="utf-8")
    image_file.write_text("image", encoding="utf-8")
    executor = RecordingFileSystemExecutor()
    command = CompressFilesCommand()
    request = command.parse(
        Namespace(
            path=str(tmp_path),
            extensions="txt",
            excluded_names=None,
        ),
        executor,
    )

    result = command.execute(request, LOGGER)

    assert result.ok
    assert result.members == (text_file,)
    assert result.archive_path.parent == tmp_path.parent
    assert result.archive_path.suffix == ".zip"
    assert executor.records[0].destination == result.archive_path
    assert executor.records[0].members == (text_file,)
    assert not result.archive_path.exists()


def test_compression_skips_when_no_files_match(tmp_path: Path) -> None:
    command = CompressFilesCommand()
    request = command.parse(
        Namespace(
            path=str(tmp_path),
            extensions="txt",
            excluded_names=None,
        ),
        RecordingFileSystemExecutor(),
    )

    result = command.execute(request, LOGGER)

    assert result.attempted == 0
    assert result.skipped == 1
    assert result.records == ()


def test_compression_reports_non_os_archive_failures(tmp_path: Path) -> None:
    (tmp_path / "member.txt").write_text("member", encoding="utf-8")

    class FailingArchiveExecutor(RecordingFileSystemExecutor):
        def create_archive(
            self,
            source: Path,
            destination: Path,
            members: Sequence[Path],
        ) -> MutationRecord:
            raise ValueError("unsupported member timestamp")

    command = CompressFilesCommand()
    request = command.parse(
        Namespace(
            path=str(tmp_path),
            extensions="txt",
            excluded_names=None,
        ),
        FailingArchiveExecutor(),
    )

    result = command.execute(request, LOGGER)

    assert result.failed == 1
    assert result.errors == (f"{result.archive_path}: unsupported member timestamp",)


def test_empty_directory_plan_ignores_directory_symlinks(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"Directory symlinks unavailable: {error}")

    command = DeleteEmptyFoldersCommand()
    result = command.execute(
        command.parse(
            Namespace(path=str(tmp_path), recursive=True),
            RecordingFileSystemExecutor(),
        ),
        LOGGER,
    )

    assert link not in result.planned_directories


def test_compression_normalizes_relative_source_before_naming_archive(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    monkeypatch.chdir(source)
    command = CompressFilesCommand()

    request = command.parse(
        Namespace(path=".", extensions=None, excluded_names=None),
        RecordingFileSystemExecutor(),
    )

    assert request.path == source.resolve()
    assert request.archive_path.parent == tmp_path
    assert request.archive_path.name.startswith("source_")
