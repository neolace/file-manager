import logging
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from Interface.CommandInterface import CommandInterface, CommandRequest, CommandResult
from Interface.FileSystemExecutor import FileSystemExecutor
from main import CommandHandler, CommandRegistry


def _delete_args(path: Path, dry_run: bool) -> Namespace:
    return Namespace(
        command="delete_by_extension",
        dry_run=dry_run,
        path=str(path),
        extensions="txt",
    )


def test_handler_selects_recording_executor_for_dry_run(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("keep", encoding="utf-8")

    exit_code = CommandHandler(logging.getLogger("test.handler")).execute(
        _delete_args(tmp_path, dry_run=True)
    )

    assert exit_code == 0
    assert target.exists()


def test_handler_selects_real_executor_for_execution(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("delete", encoding="utf-8")

    exit_code = CommandHandler(logging.getLogger("test.handler")).execute(
        _delete_args(tmp_path, dry_run=False)
    )

    assert exit_code == 0
    assert not target.exists()


@dataclass(frozen=True, kw_only=True)
class FailedRequest(CommandRequest):
    pass


class FailedCommand(CommandInterface[FailedRequest, CommandResult]):
    executed: ClassVar[bool] = False

    @property
    def description(self) -> str:
        return "Always fails"

    def parse(self, args: Namespace, executor: FileSystemExecutor) -> FailedRequest:
        return FailedRequest(executor=executor)

    def execute(self, request: FailedRequest, logger: logging.Logger) -> CommandResult:
        type(self).executed = True
        return CommandResult(
            attempted=1,
            succeeded=0,
            skipped=0,
            failed=1,
            records=(),
            errors=("failed operation",),
        )


def test_handler_returns_error_when_command_result_has_failures(
    monkeypatch,
) -> None:
    FailedCommand.executed = False
    monkeypatch.setitem(CommandRegistry.COMMAND_MAP, "failed", FailedCommand)

    exit_code = CommandHandler(logging.getLogger("test.handler")).execute(
        Namespace(command="failed", dry_run=True)
    )

    assert exit_code == 1
    assert FailedCommand.executed
