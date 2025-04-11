from pathlib import Path

from helpers import setup_logging
from helpers.delete_all_files_folders_within_folder import delete_all_files_folders_within_folder
from helpers.process_files import process_files

FILE_TYPES_TO_KEEP = [
    "jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "webp", "webm", "svg", "dng", "pdf", "mp4",
    "mov", "mp3", "sql", "txt", "pptx", "xlsx", "docx", "xls", "rtf", "zip", "csv", "log", "rar",
    "md", "tar", "ai", "ics", "db", "json", "xml", "html", "htm", "py", "js", "ts", "java", "c", "xcf",
    "cpp", "cs", "go",
    "rb", "php", "sh", "bat", "ps1", "yaml", "yml", "ini", "cfg", "conf", "xmind",
    "vcf"
]

logger = setup_logging
logger = logger.setup_logging(log_file=Path("C:/tmp/file_manager.log"))


def main(dry_run=False):
    src, dst = Path("C:/Users/terti/Downloads/bck"), Path("C:/Users/terti/OneDrive")

    logger.info(f"Source: {src}, Destination: {dst}")

    # Process files
    process_files(src, dst, file_types=FILE_TYPES_TO_KEEP, dry_run=dry_run, logger=logger)

    # Delete files and folders
    delete_all_files_folders_within_folder(src, dry_run=dry_run, logger=logger)

    logger.info("File Manager completed.")

    return 0


if __name__ == "__main__":
    exit(main())
