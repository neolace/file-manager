# Python
from pathlib import Path
from typing import Callable, Optional

def traverse_and_apply(
    path: Path,
    action: Callable[[Path], None],
    filter_func: Optional[Callable[[Path], bool]] = None,
    dry_run: bool = False,
    logger=None,
) -> None:
    """
    Traverse directories and apply an action to each item.

    Args:
        path: Root directory to traverse.
        action: Function to apply to each item.
        filter_func: Optional filter function to select items.
        dry_run: If True, only log actions without applying them.
        logger: Logger instance for output.
    """
    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    for item in path.rglob("*"):
        if filter_func and not filter_func(item):
            continue
        if dry_run:
            logger.info(f"Would apply action to: {item}")
        else:
            try:
                action(item)
                logger.info(f"Applied action to: {item}")
            except Exception as e:
                logger.error(f"Error applying action to {item}: {e}")