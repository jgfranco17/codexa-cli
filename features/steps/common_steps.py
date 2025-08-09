"""
Common step definitions for BDD tests.
"""

import json
from pathlib import Path
from typing import Optional

from behave import given, then, when

from features.steps.test_types import BehaveContext


@given("I have a testclerk CLI tool")
def step_impl_cli_tool(context: BehaveContext) -> None:
    """Verify the CLI tool is available."""
    assert context.runner is not None


@given("I am in a temporary workspace")
def step_impl_temp_workspace(context: BehaveContext) -> None:
    """Verify we're in a temporary workspace."""
    assert context.workspace is not None
    assert context.workspace.exists()


@given("I have mocked external API calls")
def step_impl_mocked_apis(context: BehaveContext) -> None:
    """Verify external API calls are mocked."""
    assert context.mock_openai is not None
    assert context.mock_api_key is not None


@when('I run the command "{command}"')
def step_impl_run_command(context: BehaveContext, command: str) -> None:
    """Run a CLI command and store the result."""
    import os

    from testclerk.main import cli

    args = command.split()

    # Change to the workspace directory and run the command
    original_cwd = os.getcwd()
    os.chdir(str(context.workspace))

    # Check if we expect an exception (set by error scenario Given steps)
    catch_exceptions = getattr(context, "expect_exception", False)

    try:
        context.result = context.runner.invoke(
            cli, args, catch_exceptions=catch_exceptions
        )
    finally:
        os.chdir(original_cwd)


@then("the command should exit with code {exit_code:d}")
def step_impl_exit_code(context: BehaveContext, exit_code: int) -> None:
    """Verify the command exit code."""
    assert (
        context.result.exit_code == exit_code
    ), f"Expected exit code {exit_code}, got {context.result.exit_code}"


@then("the output should contain {expected_text}")
def step_impl_output_contains(context: BehaveContext, expected_text: str) -> None:
    """Verify the output contains expected text."""
    # Remove quotes from expected text if present
    expected_text = expected_text.strip("\"'")

    output = context.result.output or ""
    assert (
        expected_text in output
    ), f"Expected '{expected_text}' not found in output: {output}"


@then("the output should not contain {unexpected_text}")
def step_impl_output_not_contains(context: BehaveContext, unexpected_text: str) -> None:
    """Verify the output does not contain unexpected text."""
    assert (
        unexpected_text not in context.result.output
    ), f"Unexpected '{unexpected_text}' found in output: {context.result.output}"


@then("the error output should contain {expected_error}")
def step_impl_error_contains(context: BehaveContext, expected_error: str) -> None:
    """Verify the error output contains expected text."""
    # Remove quotes from expected error if present
    expected_error = expected_error.strip("\"'")

    error_output = context.result.stderr or context.result.output or ""

    # Check if the expected error text is anywhere in the output (case insensitive)
    assert (
        expected_error.lower() in error_output.lower()
    ), f"Expected error '{expected_error}' not found in: {error_output}"


@then("a file should be created at {file_path}")
def step_impl_file_created(context: BehaveContext, file_path: str) -> None:
    """Verify a file was created at the specified path."""
    # Remove quotes if present
    file_path = file_path.strip("\"'")

    # Check in workspace if not absolute path
    file_path_obj = Path(file_path)
    if not file_path_obj.is_absolute() and hasattr(context, "workspace"):
        file_path_obj = context.workspace / file_path

    assert file_path_obj.exists(), f"File {file_path_obj} was not created"


@then("the file {file_path} should contain {expected_content}")
def step_impl_file_contains(
    context: BehaveContext, file_path: str, expected_content: str
) -> None:
    """Verify a file contains expected content."""
    # Remove quotes if present
    file_path = file_path.strip("\"'")
    expected_content = expected_content.strip("\"'")

    # Check in workspace if not absolute path
    file_path_obj = Path(file_path)
    if not file_path_obj.is_absolute() and hasattr(context, "workspace"):
        file_path_obj = context.workspace / file_path

    assert file_path_obj.exists(), f"File {file_path_obj} does not exist"
    content = file_path_obj.read_text()
    assert (
        expected_content in content
    ), f"Expected content '{expected_content}' not found in file: {content}"


@then("the OpenAI API should be called")
def step_impl_openai_called(context: BehaveContext) -> None:
    """Verify that the OpenAI API was called."""
    context.mock_openai.return_value.chat.completions.create.assert_called()


@then("the API key should be loaded")
def step_impl_api_key_loaded(context: BehaveContext) -> None:
    """Verify that the API key was loaded."""
    # Check which command was run based on the most recent command result
    # and verify the appropriate mock was called
    if hasattr(context, "result") and context.result:
        if hasattr(context, "mock_api_key_compare"):
            # For now, accept if either run or compare command called load_api_key
            try:
                context.mock_api_key.assert_called()
            except AssertionError:
                try:
                    context.mock_api_key_compare.assert_called()
                except AssertionError:
                    # Try the list command mock as well
                    context.mock_api_key_list.assert_called()
        else:
            context.mock_api_key.assert_called()
    else:
        context.mock_api_key.assert_called()


@then("pytest should be executed")
def step_impl_pytest_executed(context: BehaveContext) -> None:
    """Verify that pytest was executed."""
    context.mock_pytest.assert_called()


@then("git operations should be performed")
def step_impl_git_operations(context: BehaveContext) -> None:
    """Verify that git operations were performed."""
    context.mock_git.assert_called()
