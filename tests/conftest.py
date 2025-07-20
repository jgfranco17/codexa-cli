from pathlib import Path
from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest

from tests.tools import CommandRunner, MockLogger

RESOURCES_DIR = Path(__file__).parent / "resources"


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
    template_file = RESOURCES_DIR / "pytest_test.tpl"
    test_file = tmp_path / "test_example.py"
    contents = template_file.read_text()
    test_file.write_text(contents)
    yield test_file


@pytest.fixture
def mock_openai_client() -> Iterator[MagicMock]:
    with patch("testclerk.client.accessor.OpenAI") as mock_client:
        mock_client_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="## Summary\n- 2 passed, 1 failed"))
        ]
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_client.return_value = mock_client_instance
        yield mock_client
