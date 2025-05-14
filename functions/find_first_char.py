EMPTY_RESULT = ""


def find_first_non_whitespace(text: str | None) -> str:
    """
    Find the first non-whitespace character in a string.
    Args:
        text: The input string to search through
    Returns:
        The first non-whitespace character, or an empty string if none found
    Raises:
        TypeError: If input is None
    """
    if text is None:
        raise TypeError("Input string cannot be None")

    if not text:
        return EMPTY_RESULT

    for character in text:
        if not character.isspace():
            return character

    return EMPTY_RESULT
