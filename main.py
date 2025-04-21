import pathlib
import sys

from helpers import drop_all_empty_folders
from helpers.process_files import process_files
from helpers.setup_logging import setup_logging

FILE_TYPES_TO_KEEP = [
    "jpg",
    "jpeg",
    "png",
    "gif",
    "tif",
    "tiff",
    "bmp",
    "webp",
    "webm",
    "svg",
    "dng",
    "pdf",
    "mp4",
    "mov",
    "mp3",
    "sql",
    "txt",
    "pptx",
    "xlsx",
    "docx",
    "xls",
    "rtf",
    "zip",
    "iso",
    "csv",
    "log",
    "rar",
    "md",
    "tar",
    "ai",
    "ics",
    "db",
    "json",
    "xml",
    "html",
    "htm",
    "py",
    "js",
    "ts",
    "java",
    "c",
    "xcf",
    "cpp",
    "cs",
    "go",
    "rb",
    "php",
    "sh",
    "bat",
    "ps1",
    "yaml",
    "yml",
    "ini",
    "cfg",
    "conf",
    "xmind",
    "vcf",
]

FOLDERS_TO_REMOVE = ["pip", "node_modules"]


def main(dry_run=False):
    """
    Main function to manage files and folders.
    :param dry_run: If True, perform a dry run without making changes.
    :return:
    """

    src, dst = pathlib.Path("C:/Users/terti/OneDrive/bck"), pathlib.Path(
        "C:/Users/terti/OneDrive"
    )

    logger = setup_logging(log_file=pathlib.Path("C:/tmp/file_manager.log"))
    logger.info(f"Source: {src}, Destination: {dst}")

    # Process files
    process_files(
        src, dst, file_types=FILE_TYPES_TO_KEEP, dry_run=dry_run, logger=logger
    )

    # Delete files and folders
    # helpers.remove_folder_by_name.remove_folder_by_name(
    #  src, dry_run=dry_run, logger=logger
    # )

    # logger.info(find_all_files_recursive(src))

    drop_all_empty_folders(src, dry_run=dry_run, logger=logger)
    logger.info("File Manager completed.")

    return 0


if __name__ == "__main__":
    main()
    sys.exit()
