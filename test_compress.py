import os
import sys
import logging
from argparse import Namespace
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from functions.CompressFilesCommand import CompressFilesCommand


def main():
    # Setup logging
    logger = logging.getLogger(__file__)

    # Create a test directory with some files if it doesn't exist
    test_dir = Path("test_compress_dir")
    if not test_dir.exists():
        test_dir.mkdir()

        # Create some test files
        for i in range(5):
            (test_dir / f"test_file_{i}.txt").write_text(f"This is test file {i}")

        # Create a subdirectory with files
        sub_dir = test_dir / "subdir"
        sub_dir.mkdir()
        for i in range(3):
            (sub_dir / f"sub_file_{i}.txt").write_text(f"This is a file in subdirectory {i}")

        # Create files with different extensions
        (test_dir / "image.jpg").write_text("This is a fake image file")
        (test_dir / "document.pdf").write_text("This is a fake PDF file")

    # Create args namespace
    args = Namespace(
        path=str(test_dir),
        dry_run=True,  # Test dry run mode
        extensions="txt,pdf",  # Test extension filtering
        excluded_names="test_file_0,sub_file_1"  # Test name exclusion
    )

    # Create and execute the command
    command = CompressFilesCommand()
    try:
        command.validate(args)
        command.execute(args, logger)
        logger.info("Test completed successfully")
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
