import logging
from typing import Callable, Optional, Any

from config.Config import Config


def safe_action(
        func: Callable[..., Config.T],
        *args: Any,
        logger: logging.Logger = logging.getLogger(__name__),
        **kwargs: Any
) -> Optional[Config.T]:
    """
    Safely execute a function with error handling.

    Args:
        func: The function to execute
        *args: Positional arguments for the function
        logger: Logger instance for output
        **kwargs: Keyword arguments for the function

    Returns:
        The result of the function if successful, None if an error occurred
    """
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        logger.error(Config.ERROR_MESSAGE_FORMAT.format(func.__name__, e))
        return None
