from pathlib import Path

from functions import delete_all_files_folders_within_folder, process_files, setup_logging

FILE_TYPES_TO_KEEP = [
    "jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "webp", "webm", "svg", "dng", "pdf", "mp4",
    "mov", "mp3", "sql", "txt", "pptx", "xlsx", "docx", "xls", "rtf", "zip", "csv", "log", "rar",
    "md", "tar", "ai", "ics", "db", "json", "xml", "html", "htm", "py", "js", "ts", "java", "c",
    "cpp", "cs", "go", "rb", "php", "sh", "bat", "ps1", "yaml", "yml", "ini", "cfg", "conf", "xmind",
    "vcf"
]

# Set up the logger once
setup_logging(log_file='C:/tmp/file_manager.log')


def main(dry_run=False):
    src, dst = Path("C:/Users/terti/OneDrive/mp4/Google"), Path("C:/Users/terti/OneDrive")

    logger.Path(f"Source: {src}, Destination: {dst}")

    # Process files
    process_files(src, dst, FILE_TYPES_TO_KEEP, dry_run, logger)

    # Delete files and folders
    delete_all_files_folders_within_folder(src, FILE_TYPES_TO_KEEP, dry_run, logger)

    logger.info("File Manager completed.")


if __name__ == "__main__":
    main()
