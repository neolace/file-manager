def find_first_char(s: str) -> str:
    """
    Find the first non-whitespace character in a string.

    Args:
        s: The input string

    Returns:
        The first non-whitespace character, or an empty string if none found
    """
    if s:
        return s[0]
    else:
        return None
