class RenameFilesCommand(ProcessFilesCommandBase):
    @property
    def description(self) -> str:
        return "Rename files in a directory based on a specified pattern"

    def validate(self, args: Namespace) -> None:
        super().validate(args)
        if not getattr(args, 'rename_pattern', None):
            raise ValueError(f"'rename_pattern' parameter is required for the '{self.description}' command.")

    def _get_file_operation(self, cmd_args: Namespace, cmd_logger: logging.Logger) -> Callable[[str], None]:
        def operation_func(file_path_str: str):
            try:
                file_path = Path(file_path_str)
                new_name = cmd_args.rename_pattern.format(name=file_path.stem, ext=file_path.suffix)
                new_path = file_path.parent / new_name

                if not cmd_args.dry_run:
                    file_path.rename(new_path)
                    cmd_logger.info(f"Renamed {file_path} to {new_path}")
                else:
                    cmd_logger.info(f"[DRY RUN] Would rename {file_path} to {new_path}")
            except Exception as e:
                cmd_logger.error(f"Failed to rename {file_path_str}: {e}")

        return operation_func
