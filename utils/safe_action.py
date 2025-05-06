from typing import Callable


def safe_action(action: Callable, *args, logger=None, **kwargs):
    """
    Safely execute an action with error handling.

    Args:
        action: The function to execute.
        logger: Logger instance for output.
        *args, **kwargs: Arguments for the action.
    """
    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    try:
        action(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {action.__name__}: {e}")