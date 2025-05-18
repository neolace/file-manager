import logging
from logging import Logger
from pathlib import Path
from typing import Callable, Optional

from config.Config import Config


def get_default_logger() -> Logger:
    """Create and return a default logger instance."""
    return logging.getLogger(__name__)


def apply_action_to_item(
    item: Path, action: Callable[[Path], None], logger: Logger, dry_run: bool = False
) -> None:
    """Apply the given action to an item with proper logging."""
    if dry_run:
        logger.info(Config.LOG_WOULD_APPLY.format(item))
        return

    try:
        action(item)
        logger.info(Config.LOG_APPLIED.format(item))
    except Exception as e:
        logger.error(Config.LOG_ERROR.format(item, e))


def traverse_and_apply(
    root_path: Path,
    action: Callable[[Path], None],
    filter_func: Optional[Callable[[Path], bool]] = None,
    dry_run: bool = False,
    logger: Optional[Logger] = None,
) -> None:
    """
    Traverse directories and apply an action to each item.
    Args:
        root_path: Root directory to traverse.
        action: Function to apply to each item.
        filter_func: Optional filter function to select items.
        dry_run: If True, only log actions without applying them.
        logger: Logger instance for output.
    """
    current_logger = logger or get_default_logger()

    for item in root_path.rglob("*"):
        if filter_func and not filter_func(item):
            continue
        apply_action_to_item(item, action, current_logger, dry_run)
