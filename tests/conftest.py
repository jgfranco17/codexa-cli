import logging
from copy import deepcopy
from typing import Generator, List, Tuple
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner, Result

from testclerk.core.output import ColorHandler
from testclerk.main import cli


class TestRunner:
    def __init__(self):
        self.__runner = CliRunner()

    def run_cli(self, cli_args: List[str]) -> Result:
        """Run the project CLI with envs set."""
        return self.__runner.invoke(cli, cli_args)


class MockLogger:
    def __init__(self) -> None:
        self.logger = logging.getLogger("mock-logger")
        self.logger.setLevel(logging.DEBUG)
        self.handler = ColorHandler()
        self.logger.addHandler(self.handler)

    def get_log_and_handler(self) -> Tuple[logging.Logger, ColorHandler]:
        return self.logger, self.handler


@pytest.fixture
def runner() -> TestRunner:
    return TestRunner()


@pytest.fixture
def logger() -> MockLogger:
    return MockLogger()


@pytest.fixture
def mock_datetime() -> Generator[MagicMock, None, None]:
    with patch("testclerk.core.models.dt.datetime") as mock_datetime:
        yield mock_datetime


@pytest.fixture
def mock_docker() -> Generator[MagicMock, None, None]:
    with patch("testclerk.core.models.docker") as mock_docker:
        yield mock_docker
