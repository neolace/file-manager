import logging
import os
from argparse import Namespace
from dataclasses import FrozenInstanceError
from pathlib import Path
from types import SimpleNamespace

import pytest

from functions.CleanFolderCommand import CleanFolderCommand
from functions.DeleteByExtensionCommand import DeleteByExtensionCommand
from functions.DeleteHiddenFilesCommand import DeleteHiddenFilesCommand
from Interface.FileSystemExecutor import RecordingFileSystemExecutor
from utils.file_filter import FileFilter, HiddenMode, is_hidden

LOGGER = logging.getLogger("test.file_processing")


def test_file_filter_uses_exact_excluded_names(tmp_path: Path) -> None:
    excluded = tmp_path / "keep.txt"
    similarly_named = tmp_path / "keep.txt.backup"
    excluded.write_text("keep", encoding="utf-8")
    similarly_named.write_text("delete", encoding="utf-8")

    matches = FileFilter(excluded_names=("keep.txt",)).filter_files(tmp_path)

    assert matches == [similarly_named]


def test_file_filter_applies_excluded_extensions_and_size_bounds(
    tmp_path: Path,
) -> None:
    too_small = tmp_path / "small.txt"
    excluded_extension = tmp_path / "medium.log"
    included = tmp_path / "included.txt"
    too_large = tmp_path / "large.txt"
    too_small.write_bytes(b"1")
    excluded_extension.write_bytes(b"123")
    included.write_bytes(b"123")
    too_large.write_bytes(b"12345")

    matches = FileFilter(
        excluded_extensions=("log",),
        min_size=2,
        max_size=4,
    ).filter_files(tmp_path)

    assert matches == [included]


def test_hidden_status_is_not_inherited_from_parent_directory(
    tmp_path: Path,
) -> None:
    hidden_file = tmp_path / ".hidden"
    hidden_file.write_text("hidden", encoding="utf-8")
    hidden_directory = tmp_path / ".hidden-directory"
    hidden_directory.mkdir()
    visible_child = hidden_directory / "visible.txt"
    visible_child.write_text("visible", encoding="utf-8")

    hidden_matches = FileFilter(hidden_mode=HiddenMode.HIDDEN_ONLY).filter_files(
        tmp_path
    )
    visible_matches = FileFilter(hidden_mode=HiddenMode.VISIBLE_ONLY).filter_files(
        tmp_path
    )

    assert hidden_matches == [hidden_file]
    assert visible_matches == [visible_child]


def test_delete_by_extension_records_normalized_matches(tmp_path: Path) -> None:
    text_file = tmp_path / "notes.TXT"
    image_file = tmp_path / "image.jpg"
    text_file.write_text("text", encoding="utf-8")
    image_file.write_text("image", encoding="utf-8")
    executor = RecordingFileSystemExecutor()
    command = DeleteByExtensionCommand()
    request = command.parse(
        Namespace(path=str(tmp_path), extensions=".txt, log"), executor
    )

    result = command.execute(request, LOGGER)

    assert result.attempted == 1
    assert result.succeeded == 1
    assert result.failed == 0
    assert executor.records[0].source == text_file
    assert text_file.exists()
    assert image_file.exists()


def test_clean_folder_aggregates_delete_failures(tmp_path: Path) -> None:
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")

    class FailingExecutor(RecordingFileSystemExecutor):
        def delete_file(self, path: Path):  # type: ignore[no-untyped-def]
            if path == first:
                raise OSError("blocked")
            return super().delete_file(path)

    command = CleanFolderCommand()
    request = command.parse(
        Namespace(path=str(tmp_path), excluded_names=None), FailingExecutor()
    )

    result = command.execute(request, LOGGER)

    assert result.attempted == 2
    assert result.succeeded == 1
    assert result.failed == 1
    assert result.errors == (f"{first}: blocked",)


def test_delete_hidden_only_records_hidden_files(tmp_path: Path) -> None:
    hidden = tmp_path / ".secret"
    visible = tmp_path / "visible.txt"
    hidden.write_text("hidden", encoding="utf-8")
    visible.write_text("visible", encoding="utf-8")
    executor = RecordingFileSystemExecutor()
    command = DeleteHiddenFilesCommand()
    request = command.parse(
        Namespace(path=str(tmp_path), excluded_names=None), executor
    )

    result = command.execute(request, LOGGER)

    assert result.attempted == 1
    assert result.succeeded == 1
    assert executor.records[0].source == hidden


def test_file_filter_criteria_are_immutable() -> None:
    file_filter = FileFilter(extensions=("txt",))

    with pytest.raises(FrozenInstanceError):
        file_filter.extensions = frozenset()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        file_filter.extensions.clear()  # type: ignore[attr-defined]


@pytest.mark.skipif(os.name != "nt", reason="Windows attribute policy")
def test_hidden_detection_uses_a_links_own_windows_attributes(
    monkeypatch,
) -> None:
    path = Path("visible-link")
    hidden = SimpleNamespace(st_file_attributes=2)
    visible = SimpleNamespace(st_file_attributes=0)
    monkeypatch.setattr(Path, "stat", lambda self: hidden)
    monkeypatch.setattr(Path, "lstat", lambda self: visible)

    assert not is_hidden(path)
