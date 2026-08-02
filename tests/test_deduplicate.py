import logging
from argparse import Namespace
from pathlib import Path

import pytest

import Interface.FileSystemExecutor as executor_module
from functions.exceptions import ArgumentError
from functions.FileDeduplicator import DeduplicateCommand
from Interface.FileSystemExecutor import (
    RealFileSystemExecutor,
    RecordingFileSystemExecutor,
)

LOGGER = logging.getLogger("test.deduplicate")


def test_deduplication_plans_a_deterministic_keeper(tmp_path: Path) -> None:
    keeper = tmp_path / "a.txt"
    duplicate = tmp_path / "z.txt"
    unique = tmp_path / "unique.txt"
    keeper.write_text("same", encoding="utf-8")
    duplicate.write_text("same", encoding="utf-8")
    unique.write_text("different", encoding="utf-8")
    executor = RecordingFileSystemExecutor()
    command = DeduplicateCommand()
    request = command.parse(Namespace(directory=str(tmp_path), max_workers=2), executor)

    result = command.execute(request, LOGGER)

    assert result.total_files == 3
    assert result.unique_files == 2
    assert result.duplicates_found == 1
    assert result.plan.groups[0].keeper == keeper
    assert result.plan.groups[0].duplicates == (duplicate,)
    assert executor.records[0].source == duplicate
    assert keeper.exists()
    assert duplicate.exists()


def test_real_deduplication_removes_only_planned_duplicates(
    tmp_path: Path,
) -> None:
    keeper = tmp_path / "a.txt"
    duplicate = tmp_path / "z.txt"
    keeper.write_text("same", encoding="utf-8")
    duplicate.write_text("same", encoding="utf-8")
    command = DeduplicateCommand()
    request = command.parse(
        Namespace(directory=str(tmp_path), max_workers=1),
        RealFileSystemExecutor(),
    )

    result = command.execute(request, LOGGER)

    assert result.ok
    assert keeper.exists()
    assert not duplicate.exists()


def test_deduplicate_command_can_be_reused_without_stale_state(
    tmp_path: Path,
) -> None:
    duplicate_directory = tmp_path / "duplicates"
    duplicate_directory.mkdir()
    (duplicate_directory / "a.txt").write_text("same", encoding="utf-8")
    (duplicate_directory / "b.txt").write_text("same", encoding="utf-8")
    unique_directory = tmp_path / "unique"
    unique_directory.mkdir()
    (unique_directory / "only.txt").write_text("only", encoding="utf-8")
    command = DeduplicateCommand()

    first = command.execute(
        command.parse(
            Namespace(directory=str(duplicate_directory), max_workers=1),
            RecordingFileSystemExecutor(),
        ),
        LOGGER,
    )
    second = command.execute(
        command.parse(
            Namespace(directory=str(unique_directory), max_workers=1),
            RecordingFileSystemExecutor(),
        ),
        LOGGER,
    )

    assert first.duplicates_found == 1
    assert second.total_files == 1
    assert second.duplicates_found == 0


def test_deduplication_validates_workers_before_scanning(
    tmp_path: Path,
) -> None:
    command = DeduplicateCommand()
    request = command.parse(
        Namespace(directory=str(tmp_path), max_workers=0),
        RecordingFileSystemExecutor(),
    )

    with pytest.raises(ArgumentError, match="max_workers"):
        command.execute(request, LOGGER)


def test_deduplication_refuses_to_delete_content_changed_after_planning(
    tmp_path: Path,
) -> None:
    keeper = tmp_path / "a.txt"
    duplicate = tmp_path / "z.txt"
    keeper.write_text("same", encoding="utf-8")
    duplicate.write_text("same", encoding="utf-8")

    class ChangingExecutor(RealFileSystemExecutor):
        def delete_duplicate(
            self,
            path: Path,
            keeper_path: Path,
            expected_digest: str,
        ):
            path.write_text("changed", encoding="utf-8")
            return super().delete_duplicate(path, keeper_path, expected_digest)

    command = DeduplicateCommand()
    request = command.parse(
        Namespace(directory=str(tmp_path), max_workers=1),
        ChangingExecutor(),
    )

    result = command.execute(request, LOGGER)

    assert result.failed == 1
    assert duplicate.exists()
    assert duplicate.read_text(encoding="utf-8") == "changed"


def test_deduplication_excludes_file_symlinks(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("same", encoding="utf-8")
    link = tmp_path / "link.txt"
    try:
        link.symlink_to(target)
    except OSError as error:
        pytest.skip(f"File symlinks unavailable: {error}")
    command = DeduplicateCommand()

    result = command.execute(
        command.parse(
            Namespace(directory=str(tmp_path), max_workers=1),
            RealFileSystemExecutor(),
        ),
        LOGGER,
    )

    assert result.total_files == 1
    assert result.duplicates_found == 0
    assert target.exists()
    assert link.exists()


def test_deduplication_rechecks_keeper_after_hashing_duplicate(
    tmp_path: Path, monkeypatch
) -> None:
    keeper = tmp_path / "a.txt"
    duplicate = tmp_path / "z.txt"
    keeper.write_text("same", encoding="utf-8")
    duplicate.write_text("same", encoding="utf-8")
    original_digest = executor_module.calculate_file_digest
    calls = 0

    def mutate_keeper_after_first_digest(path: Path) -> str:
        nonlocal calls
        digest = original_digest(path)
        calls += 1
        if calls == 1:
            keeper.write_text("changed", encoding="utf-8")
        return digest

    monkeypatch.setattr(
        executor_module,
        "calculate_file_digest",
        mutate_keeper_after_first_digest,
    )
    command = DeduplicateCommand()
    request = command.parse(
        Namespace(directory=str(tmp_path), max_workers=1),
        RealFileSystemExecutor(),
    )

    result = command.execute(request, LOGGER)

    assert result.failed == 1
    assert duplicate.exists()
