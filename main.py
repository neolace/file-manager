import logging
from pathlib import Path

from functions.delete_all_files_folders_within_folder import delete_all_files_folders_within_folder
from functions.process_files import process_files
from functions.setup_logging import setup_logging

file_types_to_keep = [
    "jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "webp", "webm", "svg", "dng", "pdf", "mp4",
    "mov", "mp3", "sql", "txt", "pptx", "xlsx", "docx", "xls", "rtf", "zip", "csv", "log", "rar",
    "md", "tar", "ai", "ics", "db", "json", "xml", "html", "htm", "py", "js", "ts", "java", "c",
    "cpp", "cs", "go", "rb", "php", "sh", "bat", "ps1", "yaml", "yml", "ini", "cfg", "conf", "xmind"
]


def main(dry_run=False):
    print("Starting File Manager...")

    log_level = logging.INFO
    logger = setup_logging(log_level, log_file="C:/tmp/file_manager.log")

    src: Path = Path("C:/Users/terti/OneDrive/mp4/Google")
    dst: Path = Path("C:/Users/terti/OneDrive")

    logger.info(f"Source folder: {src}")
    logger.info(f"Destination folder: {dst}")

    process_files(src, dst, file_types_to_keep, dry_run, logger)

    delete_all_files_folders_within_folder(src, dry_run, logger)

    logger.info("File Manager completed.")


if __name__ == "__main__":
    exit(main())
