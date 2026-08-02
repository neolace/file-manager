import pytest

from Interface.CommandInterface import CommandInterface
from main import CommandRegistry


def test_registry_contains_only_working_commands() -> None:
    assert set(CommandRegistry.COMMAND_MAP) == {
        "deduplicate",
        "delete_by_extension",
        "clean_folder",
        "delete_empty",
        "delete_hidden_files",
        "compress_files",
    }


@pytest.mark.parametrize("command_name", CommandRegistry.COMMAND_MAP)
def test_every_registered_command_constructs_an_adapter(command_name: str) -> None:
    command = CommandRegistry().get_command(command_name)

    assert isinstance(command, CommandInterface)
