import io
import logging
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import Iterable, Tuple

import pytest

logger = logging.getLogger(__name__)


class TestExecutor:
    """Class for executing tests."""

    def __init__(self, test_ids: Iterable[str]):
        self.__test_ids = test_ids

    def run(self, verbose: bool = False) -> Tuple[int, str, str]:
        """Run the Pytest tests located at the specified path.

        Args:
            path (str): _description_

        Returns:
            Tuple[str, str, int]: _description_
        """
        stdout = io.StringIO()
        stderr = io.StringIO()

        pytest_base_args = []
        if verbose:
            pytest_base_args.append("-vv")

        # Redirect both stdout and stderr during the test run
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = pytest.main([*pytest_base_args, *self.__test_ids])

        # Retrieve output
        shell_output = stdout.getvalue()
        error_output = stderr.getvalue()

        return exit_code, shell_output, error_output
