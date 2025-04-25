import sys

from file_manager.parse_arguments import parse_arguments


def test_move_command_with_required_args():
    # Override sys.argv
    sys.argv = [
        "file-manager",
        "move",
        "--source",
        "/path/source",
        "--target",
        "/path/target",
        "--type",
        "pdf",
    ]
    args = parse_arguments()

    assert args.command == "move"
    assert args.source == "/path/source"
    assert args.target == "/path/target"
    assert args.type == "pdf"
    assert not args.dry_run
    assert not args.verbose


def test_delete_command_with_dry_run():
    sys.argv = [
        "file-manager",
        "delete",
        "--path",
        "/test/path",
        "--type",
        "jpg",
        "--dry-run",
    ]
    args = parse_arguments()

    assert args.command == "delete"
    assert args.path == "/test/path"
    assert args.type == "jpg"
    assert args.dry_run
    assert not args.verbose


def test_remove_command_with_verbose():
    sys.argv = [
        "file-manager",
        "remove",
        "--path",
        "/test/path",
        "--name",
        "temp",
        "--verbose",
    ]
    args = parse_arguments()

    assert args.command == "remove"
    assert args.path == "/test/path"
    assert args.name == "temp"
    assert not args.dry_run
    assert args.verbose


def test_clean_command_with_all_option():
    sys.argv = ["file-manager", "clean", "--path", "/test/path", "--all"]
    args = parse_arguments()

    assert args.command == "clean"
    assert args.path == "/test/path"
    assert args.all
    assert not args.verbose


def test_extract_command_with_custom_7zip_path():
    sys.argv = [
        "file-manager",
        "extract",
        "--path",
        "/archives",
        "--7zip",
        "/custom/7z.exe",
    ]
    args = parse_arguments()

    assert args.command == "extract"
    assert args.path == "/archives"
    assert args._7zip == "/custom/7z.exe"


def test_copy_command_with_dry_run_and_verbose():
    sys.argv = [
        "file-manager",
        "copy",
        "--source",
        "/src",
        "--target",
        "/dest",
        "--type",
        "mp3",
        "--dry-run",
        "--verbose",
    ]
    args = parse_arguments()

    assert args.command == "copy"
    assert args.source == "/src"
    assert args.target == "/dest"
    assert args.type == "mp3"
    assert args.dry_run
    assert args.verbose


def test_find_dupes_command():
    sys.argv = ["file-manager", "find-dupes", "--path", "/test/folder"]
    args = parse_arguments()

    assert args.command == "find-dupes"
    assert args.path == "/test/folder"


def test_organize_date_command_with_custom_format():
    sys.argv = [
        "file-manager",
        "organize-date",
        "--source",
        "/photos",
        "--target",
        "/archive",
        "--format",
        "%Y/%m/%d",
    ]
    args = parse_arguments()

    assert args.command == "organize-date"
    assert args.source == "/photos"
    assert args.target == "/archive"
    assert args.format == "%Y/%m/%d"
    assert not args.use_created


def test_search_command_with_extensions():
    sys.argv = [
        "file-manager",
        "search",
        "--path",
        "/docs",
        "--text",
        "important",
        "--extensions",
        "txt",
        "md",
        "doc",
    ]
    args = parse_arguments()

    assert args.command == "search"
    assert args.path == "/docs"
    assert args.text == "important"
    assert args.extensions == ["txt", "md", "doc"]
    assert not args.case_sensitive


def test_process_extensions_command():
    sys.argv = ["file-manager", "process-extensions", "--path", "/files", "--dry-run"]
    args = parse_arguments()

    assert args.command == "process-extensions"
    assert args.path == "/files"
    assert args.dry_run
