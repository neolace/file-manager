import os


def process_files(operation, path, extensions=None, excluded_names=None, dry_run=False, recursive=True, log_file=None):
    if not callable(operation):
        raise ValueError("The 'operation' parameter must be a callable function.")

    if not os.path.isdir(path):
        raise ValueError(f"The path '{path}' is not a valid directory.")

    if extensions is not None and not isinstance(extensions, (list, tuple)):
        raise ValueError("The 'extensions' parameter must be a list or tuple.")

    if excluded_names is not None and not isinstance(excluded_names, (list, tuple)):
        raise ValueError("The 'excluded_names' parameter must be a list or tuple.")

    def should_process(f_name):
        if extensions and isinstance(extensions, (list, tuple)) and not any(f_name.endswith(ext) for ext in extensions):
            return False
        if excluded_names and isinstance(excluded_names, (list, tuple)) and f_name in excluded_names:
            return False
        return True

    def log(message):
        if log_file:
            try:
                with open(log_file, 'a', encoding='utf-8') as log:
                    log.write(message + '\n')
            except OSError as e:
                print(f"Error writing to log file '{log_file}': {e}")
        else:
            print(message)

    try:
        for root, dirs, files in os.walk(path):
            if not recursive:
                dirs.clear()  # Prevent descending into subdirectories

            for file_name in files:
                if should_process(file_name):
                    file_path = os.path.join(root, file_name)
                    if dry_run:
                        log(f"[DRY RUN] Would process: {file_path}")
                    else:
                        try:
                            operation(file_path)
                            log(f"Processed: {file_path}")
                        except Exception as e:
                            log(f"Error processing {file_path}: {e}")
    except Exception as e:
        log(f"Error traversing directory '{path}': {e}")
