import os
from pathlib import Path
from typing import List


def assert_files_created(working_dir: str, files: List[str]) -> None:
    """Assert that the expected files to be generated are created."""
    for file in files:
        full_path = Path(os.path.join(working_dir, file))
        assert full_path.exists(), f"Templated file '{str(full_path)}' was not created"


def assert_lines_in_file(filename: str, expected_lines: List[str]) -> None:
    """Assert that the expected lines are found in the file."""
    with open(filename, "r") as file:
        contents = file.read()
        for line in expected_lines:
            assert line in contents, f"Line not found in {filename}: '{line}'"
