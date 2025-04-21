def delete_empty_folders(path, dry_run: bool = False, logger=None) -> None:
    """
    Recursively loop through all folders and subfolders in the given path,
    deleting only empty folders. Default path is the current working directory.
    """
    try:
        # Iterate through all items in the current path
        for item in path.iterdir():
            # Check if the item is a directory
            if item.is_dir():
                # Recursively process subfolders first
                delete_empty_folders(item)
                # After processing subfolders, check if the current folder is empty
                try:
                    item.rmdir()  # rmdir only deletes empty directories
                    print(f"Deleted empty folder: {item}")
                except OSError:
                    # Folder is not empty or cannot be deleted, skip silently
                    pass
    except OSError as e:
        print(f"Error accessing {path}: {e}")
