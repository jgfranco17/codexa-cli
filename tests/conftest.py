from pathlib import Path
from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest

from tests.tools import CommandRunner, MockLogger


@pytest.fixture
def runner() -> CommandRunner:
    return CommandRunner()


@pytest.fixture
def logger() -> MockLogger:
    return MockLogger()


@pytest.fixture
def mock_datetime() -> Iterator[MagicMock]:
    with patch("testclerk.core.models.dt.datetime") as mock_datetime:
        yield mock_datetime


@pytest.fixture
def mock_pytest_file(tmp_path: Path) -> Iterator[Path]:
    """Mock a pytest file."""
    template_file = Path(__file__).parent / "resources" / "pytest_test.tpl"
    test_file = tmp_path / "test_example.py"
    contents = template_file.read_text()
    test_file.write_text(contents)
    yield test_file
