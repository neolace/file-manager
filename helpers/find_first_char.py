from typing import Optional


def find_first_char(string: str) -> Optional[str]:
    """
    Return the first character of a string, or None if the string is empty.

    Args:
        string: The input string

    Returns:
        The first character or None if string is empty
    """
    if string:
        return string[0]
    else:
        return None
