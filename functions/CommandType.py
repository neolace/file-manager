from enum import Enum, auto


class CommandType(Enum):
    """Supported command types"""
    DEDUPLICATE = auto()
    MOVE = auto()
    DELETE_BY_EXTENSION = auto()
    CLEAN_FOLDER = auto()
    DELETE_EMPTY = auto()
    DELETE_HIDDEN_FILES = auto()  # Renamed from DELETE_HIDDEN

