"""
Behave environment configuration for BDD tests.
Sets up test fixtures and mocking for external API calls.
"""

import os
import tempfile
from pathlib import Path
from typing import Iterator
from unittest.mock import MagicMock, patch

from behave import fixture, use_fixture
from click.testing import CliRunner

from features.steps.test_types import BehaveContext, MockConfig


@fixture
def cli_runner(context: BehaveContext) -> Iterator[CliRunner]:
    """Provide a CLI runner for testing commands."""
    context.runner = CliRunner()
    yield context.runner


@fixture
def temp_workspace(context: BehaveContext) -> Iterator[Path]:
    """Provide a temporary workspace for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        context.workspace = Path(temp_dir)
        context.original_cwd = os.getcwd()

        # Create necessary subdirectories
        (context.workspace / "tests").mkdir(exist_ok=True)

        # Create a minimal test file for testing
        test_file = context.workspace / "test_example.py"
        test_file.write_text(
            """
def test_example():
    assert True

def test_another():
    assert 1 + 1 == 2
"""
        )

        yield context.workspace


@fixture
def mock_openai_api(context: BehaveContext) -> Iterator[MagicMock]:
    """Mock OpenAI API calls to prevent external API calls during testing."""
    with patch("testclerk.client.accessor.OpenAI") as mock_client:
        mock_client_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content="## Test Report\n- All tests passed successfully"
                )
            )
        ]
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_client.return_value = mock_client_instance
        context.mock_openai = mock_client
        yield mock_client


@fixture
def mock_api_key(context: BehaveContext) -> Iterator[MagicMock]:
    """Mock API key loading to avoid requiring real API keys."""
    # Need to patch in the modules where it's imported, not where it's defined
    with patch("testclerk.commands.run.load_api_key") as mock_run_key, patch(
        "testclerk.commands.compare.load_api_key"
    ) as mock_compare_key, patch(
        "testclerk.commands.list.load_api_key"
    ) as mock_list_key:

        # All should return the same test key
        test_key = "test-api-key-12345"
        mock_run_key.return_value = test_key
        mock_compare_key.return_value = test_key
        mock_list_key.return_value = test_key

        # Store the run command mock for assertions (most commonly used)
        context.mock_api_key = mock_run_key
        context.mock_api_key_compare = mock_compare_key
        context.mock_api_key_list = mock_list_key

        yield mock_run_key


@fixture
def mock_pytest_execution(context: BehaveContext) -> Iterator[MagicMock]:
    """Mock pytest execution to avoid running actual tests."""
    with patch("testclerk.client.executor.pytest.main") as mock_pytest, patch(
        "subprocess.run"
    ) as mock_subprocess:

        mock_pytest.return_value = 0  # Success exit code

        # Mock subprocess for pytest commands
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "collected 2 items\n\ntest_example.py::test_example PASSED\ntest_example.py::test_another PASSED\n\n1. test_example.py::test_example\n2. test_example.py::test_another"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        context.mock_pytest = mock_pytest
        context.mock_subprocess = mock_subprocess
        yield mock_pytest


@fixture
def mock_git_operations(context: BehaveContext) -> Iterator[MagicMock]:
    """Mock git operations to avoid requiring a git repository."""
    with patch("testclerk.commands.compare.compare_git_diff") as mock_git:
        mock_git.return_value = "diff --git a/test_file.py b/test_file.py\n+ def new_test_function():\n+     pass"
        context.mock_git = mock_git
        yield mock_git


@fixture
def mock_file_operations(context: BehaveContext) -> Iterator[None]:
    """Mock file operations to redirect writes to the workspace."""
    from pathlib import Path

    original_open = open

    def mock_open_function(file_path, mode="r", **kwargs):
        """Mock open function that redirects file writes to workspace."""
        path = Path(file_path) if not isinstance(file_path, Path) else file_path

        # If this is a write operation and the path looks like a report file, redirect to workspace
        if "w" in mode and hasattr(context, "workspace"):
            if path.name.endswith(".md") and path.name in [
                "report.md",
                "custom_report.md",
                "diff_report.md",
                "custom_diff.md",
            ]:
                # Redirect to workspace
                workspace_path = context.workspace / path.name
                return original_open(workspace_path, mode, **kwargs)

        # For all other operations, use the original path
        return original_open(file_path, mode, **kwargs)

    # Mock Path.write_text as well for compare command
    original_write_text = Path.write_text

    def mock_write_text(self, data, encoding=None, errors=None, newline=None):
        """Mock Path.write_text to redirect to workspace."""
        if hasattr(context, "workspace") and self.name.endswith(".md"):
            if self.name in [
                "report.md",
                "custom_report.md",
                "diff_report.md",
                "custom_diff.md",
            ]:
                workspace_path = context.workspace / self.name
                return original_write_text(
                    workspace_path, data, encoding, errors, newline
                )
        return original_write_text(self, data, encoding, errors, newline)

    with patch("builtins.open", side_effect=mock_open_function), patch.object(
        Path, "write_text", mock_write_text
    ):
        yield


def before_scenario(context: BehaveContext, scenario) -> None:
    """Set up fixtures before each scenario."""
    use_fixture(cli_runner, context)
    use_fixture(temp_workspace, context)
    use_fixture(mock_openai_api, context)
    use_fixture(mock_api_key, context)
    use_fixture(mock_pytest_execution, context)
    use_fixture(mock_git_operations, context)
    use_fixture(mock_file_operations, context)


def after_scenario(context: BehaveContext, scenario) -> None:
    """Clean up after each scenario."""
    if hasattr(context, "workspace") and context.workspace.exists():
        import shutil

        shutil.rmtree(context.workspace, ignore_errors=True)
