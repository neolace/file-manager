import shutil
from pathlib import Path


def drop_all_empty_folders(
    root_path: Path, remove_all: bool = False, logger: None = None
) -> None:
    """
    Recursively delete all empty folders under the given root path.
    :param root_path:
    :param remove_all:
    :param logger:
    :return:
    """

    root_path = Path(root_path)
    deleted_count = 0

    if remove_all:
        # Delete everything under root
        for item in root_path.iterdir():
            if item.is_dir():
                try:
                    shutil.rmtree(item)
                    deleted_count += 1
                    logger.info(f"Deleted folder and contents: {item}")
                except OSError as e:
                    logger.error(f"Error deleting {item}: {e}")
    else:
        # Delete empty folders only, bottom-up
        for folder in sorted(
            root_path.rglob("*"), key=lambda x: len(str(x)), reverse=True
        ):
            if folder.is_dir() and not any(folder.iterdir()):
                try:
                    folder.rmdir()  # Use rmdir for empty directories instead of rmtree
                    deleted_count += 1
                    logger.info(f"Deleted empty folder: {folder}")
                except OSError as e:
                    logger.error(f"Error deleting {folder}: {e}")

    logger.info(f"Cleaned {deleted_count} folders")
