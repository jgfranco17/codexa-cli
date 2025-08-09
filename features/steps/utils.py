"""
Utility functions for BDD tests with type safety.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from features.steps.test_types import (
    BehaveContext,
    CommandAssertion,
    FileAssertion,
    MockConfig,
    TestResult,
)


def create_mock_config(
    api_response: str = "## Test Report\n- All tests passed successfully",
    api_error: Optional[str] = None,
    pytest_exit_code: int = 0,
    git_diff: str = "diff --git a/test_file.py b/test_file.py\n+ def new_test_function():\n+     pass",
    api_key: str = "test-api-key-12345",
) -> MockConfig:
    """Create a mock configuration with type safety."""
    return MockConfig(
        api_response=api_response,
        api_error=api_error,
        pytest_exit_code=pytest_exit_code,
        git_diff=git_diff,
        api_key=api_key,
    )


def create_command_assertion(
    expected_exit_code: int,
    expected_output: Optional[str] = None,
    expected_error: Optional[str] = None,
    should_create_file: Optional[Union[str, Path]] = None,
) -> CommandAssertion:
    """Create a command assertion with type safety."""
    file_path = Path(should_create_file) if should_create_file else None
    return CommandAssertion(
        expected_exit_code=expected_exit_code,
        expected_output=expected_output,
        expected_error=expected_error,
        should_create_file=file_path,
    )


def create_file_assertion(
    path: Union[str, Path], expected_content: Optional[str] = None
) -> FileAssertion:
    """Create a file assertion with type safety."""
    file_path = Path(path) if isinstance(path, str) else path
    return FileAssertion(path=file_path, expected_content=expected_content)


def verify_command_result(context: BehaveContext, assertion: CommandAssertion) -> None:
    """Verify command execution results with type safety."""
    if context.result is None:
        raise ValueError("No command result available")

    # Check exit code
    assert (
        context.result.exit_code == assertion.expected_exit_code
    ), f"Expected exit code {assertion.expected_exit_code}, got {context.result.exit_code}"

    # Check output
    if assertion.expected_output:
        assert (
            assertion.expected_output in context.result.output
        ), f"Expected output '{assertion.expected_output}' not found in: {context.result.output}"

    # Check error output
    if assertion.expected_error:
        error_output = context.result.stderr or context.result.output
        assert (
            assertion.expected_error in error_output
        ), f"Expected error '{assertion.expected_error}' not found in: {error_output}"

    # Check file creation
    if assertion.should_create_file:
        assert (
            assertion.should_create_file.exists()
        ), f"Expected file {assertion.should_create_file} was not created"


def verify_file_content(file_assertion: FileAssertion) -> None:
    """Verify file content with type safety."""
    assert file_assertion.path.exists(), f"File {file_assertion.path} does not exist"

    if file_assertion.expected_content:
        content = file_assertion.path.read_text()
        assert (
            file_assertion.expected_content in content
        ), f"Expected content '{file_assertion.expected_content}' not found in file: {content}"


def setup_mock_responses(context: BehaveContext, config: MockConfig) -> None:
    """Setup mock responses with type safety."""
    # Setup OpenAI API mock
    if config.api_error:
        context.mock_openai.return_value.chat.completions.create.side_effect = (
            Exception(config.api_error)
        )
    else:
        mock_response = (
            context.mock_openai.return_value.chat.completions.create.return_value
        )
        mock_response.choices[0].message.content = config.api_response

    # Setup API key mock
    context.mock_api_key.return_value = config.api_key

    # Setup pytest mock
    context.mock_pytest.return_value = config.pytest_exit_code

    # Setup git mock
    context.mock_git.return_value = config.git_diff


def get_test_data(context: BehaveContext, key: str, default: Any = None) -> Any:
    """Get test data with type safety."""
    if not hasattr(context, "test_data"):
        context.test_data = {}
    return context.test_data.get(key, default)


def set_test_data(context: BehaveContext, key: str, value: Any) -> None:
    """Set test data with type safety."""
    if not hasattr(context, "test_data"):
        context.test_data = {}
    context.test_data[key] = value


def create_test_result(exit_code: int, output: str, stderr: str = "") -> TestResult:
    """Create a test result with type safety."""
    return TestResult(exit_code=exit_code, output=output, stderr=stderr)


def validate_context(context: BehaveContext) -> None:
    """Validate that the context has all required attributes."""
    required_attrs = [
        "runner",
        "workspace",
        "mock_openai",
        "mock_api_key",
        "mock_pytest",
        "mock_git",
    ]

    missing_attrs = [attr for attr in required_attrs if not hasattr(context, attr)]
    if missing_attrs:
        raise ValueError(f"Missing required context attributes: {missing_attrs}")


def get_workspace_path(context: BehaveContext) -> Path:
    """Get the workspace path with type safety."""
    if not hasattr(context, "workspace") or context.workspace is None:
        raise ValueError("Workspace not initialized")
    workspace = context.workspace
    assert isinstance(workspace, Path)
    return workspace


def create_test_file(context: BehaveContext, filename: str, content: str = "") -> Path:
    """Create a test file in the workspace with type safety."""
    workspace = get_workspace_path(context)
    file_path = workspace / filename
    file_path.write_text(content)
    return file_path


def cleanup_test_files(context: BehaveContext) -> None:
    """Clean up test files with type safety."""
    if hasattr(context, "workspace") and context.workspace.exists():
        import shutil

        shutil.rmtree(context.workspace, ignore_errors=True)
