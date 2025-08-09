"""
Type definitions for Behave BDD tests.
Provides type hints for better IDE support and code quality.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union
from unittest.mock import MagicMock

from behave.runner import Context
from click.testing import CliRunner, Result


class BehaveContext(Context):
    """Extended context class with type hints for all test fixtures and mocks."""

    # CLI testing
    runner: CliRunner
    result: Optional[Result]

    # Workspace and file system
    workspace: Path
    original_cwd: str

    # Mocked external dependencies
    mock_openai: MagicMock
    mock_api_key: MagicMock
    mock_pytest: MagicMock
    mock_git: MagicMock

    # Test data and state
    test_data: Dict[str, Any]
    scenario_name: str
    feature_name: str


class TestResult:
    """Type for test execution results."""

    def __init__(self, exit_code: int, output: str, stderr: str = ""):
        self.exit_code = exit_code
        self.output = output
        self.stderr = stderr


class MockConfig:
    """Configuration for mocked responses."""

    def __init__(
        self,
        api_response: str = "## Test Report\n- All tests passed successfully",
        api_error: Optional[str] = None,
        pytest_exit_code: int = 0,
        git_diff: str = "diff --git a/test_file.py b/test_file.py\n+ def new_test_function():\n+     pass",
        api_key: str = "test-api-key-12345",
    ):
        self.api_response = api_response
        self.api_error = api_error
        self.pytest_exit_code = pytest_exit_code
        self.git_diff = git_diff
        self.api_key = api_key


class FileAssertion:
    """Type for file-related assertions."""

    def __init__(self, path: Path, expected_content: Optional[str] = None):
        self.path = path
        self.expected_content = expected_content


class CommandAssertion:
    """Type for command execution assertions."""

    def __init__(
        self,
        expected_exit_code: int,
        expected_output: Optional[str] = None,
        expected_error: Optional[str] = None,
        should_create_file: Optional[Path] = None,
    ):
        self.expected_exit_code = expected_exit_code
        self.expected_output = expected_output
        self.expected_error = expected_error
        self.should_create_file = should_create_file
