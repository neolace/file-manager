import logging
from pathlib import Path

from functions.delete_all_files_folders_within_folder import delete_all_files_folders_within_folder
from functions.move_files_by_extension import move_files_by_extension
from functions.setup_logging import setup_logging


def main(dry_run=False):
    print("Starting File Manager...")

    log_level = logging.INFO
    logger = setup_logging(log_level, log_file="C:/Users/terti/OneDrive/mp4/Google/file_manager.log")

    ft = ["jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "webp", "webm", "svg", "dng",
          "pdf", "mp4", "mov", "mp3", "sql", "txt", "pptx", "xlsx", "docx",
          "xlsx", "xls", "doc", "xls", "rtf", "zip", "csv", "log", "rar",
          "md", "tar", "ai", "ics", "db", 'txt', 'log', 'md', 'csv', 'json', 'xml', 'html', 'htm',
          'py', 'js', 'ts', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php',
          'sh', 'bat', 'ps1', 'yaml', 'yml', 'ini', 'cfg', 'conf']

    src = Path(f"C:/Users/terti/OneDrive/mp4/Google/gbck")
    dst = Path(f"C:/Users/terti/OneDrive/mp4/Google")

    logger.info(f"Source folder: {src}")
    logger.info(f"Destination folder: {dst}")

    for ftc in ft:
        dst_combined = Path(dst.joinpath(ftc))
        logger.info(f"Destination folder: {dst_combined}")
        if dry_run:
            break
        move_files_by_extension(source_folder=src, target_folder=dst_combined, file_type=ftc, logger=logger,
                                dry_run=dry_run)

    delete_all_files_folders_within_folder(dry_run=dry_run, logger=logger, folder_path=src)


if __name__ == "__main__":
    exit(main())
