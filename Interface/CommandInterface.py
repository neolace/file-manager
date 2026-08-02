import logging
from abc import ABC, abstractmethod
from argparse import Namespace
from dataclasses import dataclass
from typing import Generic, Tuple, TypeVar

from Interface.FileSystemExecutor import FileSystemExecutor, MutationRecord


@dataclass(frozen=True, kw_only=True)
class CommandRequest:
    executor: FileSystemExecutor


@dataclass(frozen=True, kw_only=True)
class CommandResult:
    attempted: int
    succeeded: int
    skipped: int
    failed: int
    records: Tuple[MutationRecord, ...]
    errors: Tuple[str, ...]

    @property
    def ok(self) -> bool:
        return self.failed == 0


RequestT = TypeVar("RequestT", bound=CommandRequest)
ResultT = TypeVar("ResultT", bound=CommandResult)


class CommandInterface(ABC, Generic[RequestT, ResultT]):
    """Base interface for all commands"""

    @abstractmethod
    def parse(self, args: Namespace, executor: FileSystemExecutor) -> RequestT:
        pass

    @abstractmethod
    def execute(self, request: RequestT, logger: logging.Logger) -> ResultT:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
