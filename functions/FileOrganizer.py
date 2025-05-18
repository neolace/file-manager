import datetime
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class OrganizerConfig:
    root_path: Path
    target_folder: Path
    date_format: str = "%Y-%m"
    use_modified_date: bool = True
    dry_run: bool = False
    logger: Optional[logging.Logger] = None


class FileOrganizer:
    def __init__(self, config: OrganizerConfig):
        self.config = config
        self.logger = config.logger or logging.getLogger(__name__)
        self.organized_count = 0

    def organize_files(self) -> None:
        """Main method to organize files by date."""
        if not self._validate_source_folder():
            return

        try:
            files = self._get_files()
            self.logger.info(f"Found {len(files)} files to organize")
            self._ensure_target_folder()

            for file in files:
                self._process_file(file)

            self._log_summary()
        except OSError as e:
            self.logger.error(f"Error organizing files by date: {e}")

    def _validate_source_folder(self) -> bool:
        """Check if the source folder exists."""
        if not self.config.root_path.exists():
            self.logger.error(f"Source folder does not exist: {self.config.root_path}")
            return False
        return True

    def _get_files(self) -> List[Path]:
        """Get all files from the source folder."""
        return [f for f in self.config.root_path.rglob("*") if f.is_file()]

    def _ensure_target_folder(self) -> None:
        """Create a target folder if it doesn't exist and not in dry run mode."""
        if not self.config.dry_run and not self.config.target_folder.exists():
            self.config.target_folder.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created target directory: {self.config.target_folder}")

    def _get_file_timestamp(self, file: Path) -> datetime.datetime:
        """Get file timestamp based on configuration."""
        stat = file.stat()
        timestamp = stat.st_mtime if self.config.use_modified_date else stat.st_ctime
        return datetime.datetime.fromtimestamp(timestamp)

    def _get_target_path(self, file: Path, date_folder: Path) -> Path:
        """Generate a unique target path for a file."""
        target_path = date_folder / file.name
        counter = 1
        while not self.config.dry_run and target_path.exists():
            target_path = date_folder / f"{file.stem}_{counter}{file.suffix}"
            counter += 1
        return target_path

    def _process_file(self, file: Path) -> None:
        """Process single file organization."""
        timestamp = self._get_file_timestamp(file)
        date_folder_name = timestamp.strftime(self.config.date_format)
        date_folder = self.config.target_folder / date_folder_name
        target_path = self._get_target_path(file, date_folder)

        if self.config.dry_run:
            self.logger.info(f"Would organize {file} to {date_folder / file.name}")
            return

        if not date_folder.exists():
            date_folder.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created date folder: {date_folder}")

        try:
            shutil.copy2(file, target_path)
            self.organized_count += 1
            self.logger.info(f"Organized {file} to {target_path}")
        except OSError as e:
            self.logger.error(f"Failed to organize {file}: {e}")

    def _log_summary(self) -> None:
        """Log organization summary."""
        action = "Would organize" if self.config.dry_run else "Organized"
        self.logger.info(f"{action} {self.organized_count} files")


def organize_files_by_date(
    root_path: Path,
    target_folder: Path,
    date_format: str = "%Y-%m",
    use_modified_date: bool = True,
    dry_run: bool = False,
    logger: Optional[logging.Logger] = None,
) -> None:
    config = OrganizerConfig(
        root_path=Path(root_path),
        target_folder=Path(target_folder),
        date_format=date_format,
        use_modified_date=use_modified_date,
        dry_run=dry_run,
        logger=logger,
    )
    organizer = FileOrganizer(config)
    organizer.organize_files()
