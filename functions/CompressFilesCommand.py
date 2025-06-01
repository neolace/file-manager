import zipfile
from pathlib import Path

from main import CommandInterface


class CompressFilesCommand(CommandInterface):
    @property
    def description(self) -> str:
        return "Compress files in a directory into a .zip archive"

    def validate(self, args: Namespace) -> None:
        if not args.path:
            raise ValueError(f"'path' argument is required for the '{self.description}' command.")
        if not args.output_file:
            raise ValueError(f"'output_file' argument is required for the '{self.description}' command.")
        path_obj = Path(args.path)
        if not path_obj.exists() or not path_obj.is_dir():
            raise ValueError(f"Path is not a valid directory: {args.path}")

    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        try:
            output_file = Path(args.output_file)
            with zipfile.ZipFile(output_file, 'w') as zipf:
                for root, _, files in os.walk(args.path):
                    for file_name in files:
                        file_path = Path(root) / file_name
                        zipf.write(file_path, file_path.relative_to(args.path))
                        logger.info(f"Compressed: {file_path}")
            logger.info(f"Files compressed into {output_file}")
        except Exception as e:
            logger.error(f"Failed to compress files: {e}")
