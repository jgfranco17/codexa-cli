import logging
from copy import deepcopy
from typing import List, Optional, Tuple

import pytest
from click.testing import CliRunner, Result

from codexa.core.output import ColorHandler
from codexa.main import cli


class CommandRunner:
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


def verify_cli_output(
    result: Result,
    expected_exit_code: int,
    expected_stdout: Optional[str] = None,
    expected_stderr: Optional[str] = None,
) -> None:
    """Verify the CLI output from test execution."""
    assert (
        result.exit_code == expected_exit_code
    ), f"Expected {expected_exit_code}, got {result.exit_code}"
    if expected_stdout:
        assert (
            expected_stdout in result.output
        ), f"Expected output '{expected_stdout}' not found in stdout, got: {result.output}"
    if expected_stderr:
        assert (
            expected_stderr in result.stderr
        ), f"Expected output '{expected_stderr}' not found in stdout, got: {result.output}"
