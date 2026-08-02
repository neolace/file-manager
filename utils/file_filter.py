import os
import stat
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import FrozenSet, Optional, Sequence, Union


class HiddenMode(Enum):
    ANY = auto()
    VISIBLE_ONLY = auto()
    HIDDEN_ONLY = auto()


def is_hidden(file_path: Path) -> bool:
    if file_path.name.startswith("."):
        return True
    if os.name != "nt":
        return False
    attributes = getattr(file_path.lstat(), "st_file_attributes", 0)
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 2))


@dataclass(frozen=True, init=False)
class FileFilter:
    extensions: FrozenSet[str]
    excluded_names: FrozenSet[str]
    excluded_extensions: FrozenSet[str]
    min_size: Optional[int]
    max_size: Optional[int]
    hidden_mode: HiddenMode

    def __init__(
        self,
        extensions: Optional[Sequence[str]] = None,
        excluded_names: Optional[Sequence[str]] = None,
        excluded_extensions: Optional[Sequence[str]] = None,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        hidden_mode: HiddenMode = HiddenMode.ANY,
    ) -> None:
        object.__setattr__(self, "extensions", self._normalize_extensions(extensions))
        object.__setattr__(self, "excluded_names", frozenset(excluded_names or ()))
        object.__setattr__(
            self,
            "excluded_extensions",
            self._normalize_extensions(excluded_extensions),
        )
        object.__setattr__(self, "min_size", min_size)
        object.__setattr__(self, "max_size", max_size)
        object.__setattr__(self, "hidden_mode", hidden_mode)

    @staticmethod
    def _normalize_extensions(
        extensions: Optional[Sequence[str]],
    ) -> FrozenSet[str]:
        return frozenset(
            extension.lower().lstrip(".") for extension in extensions or () if extension
        )

    def matches(self, file_path: Path) -> bool:
        if not file_path.is_file():
            return False
        if file_path.name in self.excluded_names:
            return False

        extension = file_path.suffix.lower().lstrip(".")
        if self.excluded_extensions and extension in self.excluded_extensions:
            return False
        if self.extensions and extension not in self.extensions:
            return False

        size = file_path.stat().st_size
        if self.min_size is not None and size < self.min_size:
            return False
        if self.max_size is not None and size > self.max_size:
            return False

        hidden = is_hidden(file_path)
        if self.hidden_mode is HiddenMode.VISIBLE_ONLY and hidden:
            return False
        if self.hidden_mode is HiddenMode.HIDDEN_ONLY and not hidden:
            return False
        return True

    def filter_files(
        self, directory: Union[str, Path], recursive: bool = True
    ) -> list[Path]:
        directory_path = Path(directory)
        if not directory_path.is_dir():
            raise ValueError(f"Not a directory: {directory}")

        files = directory_path.rglob("*") if recursive else directory_path.glob("*")
        return sorted(
            (path for path in files if self.matches(path)),
            key=lambda path: os.path.normcase(str(path.resolve())),
        )
