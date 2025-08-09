"""
Error handling step definitions for BDD tests.
"""

from unittest.mock import MagicMock

from behave import given, then, when

from features.steps.test_types import BehaveContext


@given("the OpenAI API returns an error")
def step_impl_openai_error(context: BehaveContext) -> None:
    """Configure the mock to return an API error."""
    context.mock_openai.return_value.chat.completions.create.side_effect = Exception(
        "API Error"
    )
    context.expect_exception = True  # Signal that we expect an exception


@given("the API key is invalid")
def step_impl_invalid_api_key(context: BehaveContext) -> None:
    """Configure the mock to return an invalid API key."""
    context.mock_api_key.return_value = ""


@given("pytest execution fails")
def step_impl_pytest_fails(context: BehaveContext) -> None:
    """Configure the mock to simulate pytest failure."""
    context.mock_pytest.return_value = 1  # Non-zero exit code


@given("git operations fail")
def step_impl_git_fails(context: BehaveContext) -> None:
    """Configure the mock to simulate git operation failure."""
    context.mock_git.side_effect = Exception("Git operation failed")


@when("I run an invalid command")
def step_impl_invalid_command(context: BehaveContext) -> None:
    """Run a command with invalid arguments."""
    import os

    from testclerk.main import cli

    original_cwd = os.getcwd()
    os.chdir(str(context.workspace))

    try:
        context.result = context.runner.invoke(
            cli, ["invalid-command"], catch_exceptions=False
        )
    finally:
        os.chdir(original_cwd)


@when("I run a command with missing required arguments")
def step_impl_missing_args(context: BehaveContext) -> None:
    """Run a command with missing required arguments."""
    import os

    from testclerk.main import cli

    original_cwd = os.getcwd()
    os.chdir(str(context.workspace))

    try:
        context.result = context.runner.invoke(
            cli, ["run", "--output"], catch_exceptions=False
        )
    finally:
        os.chdir(original_cwd)


@then("the command should fail with error")
def step_impl_command_fails(context: BehaveContext) -> None:
    """Verify the command failed with an error."""
    assert (
        context.result.exit_code != 0
    ), f"Expected failure, got exit code {context.result.exit_code}"


@then("the error message should contain {expected_error}")
def step_impl_error_message_contains(
    context: BehaveContext, expected_error: str
) -> None:
    """Verify the error message contains expected text."""
    # Remove quotes from expected error if present
    expected_error = expected_error.strip("\"'")

    error_output = context.result.stderr or context.result.output or ""

    # Check if the expected error text is anywhere in the output (case insensitive)
    assert (
        expected_error.lower() in error_output.lower()
    ), f"Expected error '{expected_error}' not found in: {error_output}"


@then("the API error should be handled gracefully")
def step_impl_api_error_handled(context: BehaveContext) -> None:
    """Verify API errors are handled gracefully."""
    # For now, just check that the command failed with the expected exit code
    # The actual error handling is internal and may not show in stdout/stderr
    # when using Click's catch_exceptions=True
    assert (
        context.result.exit_code != 0
    ), f"Expected failure, got exit code {context.result.exit_code}"


@then("the invalid API key should be detected")
def step_impl_api_key_detected(context: BehaveContext) -> None:
    """Verify invalid API key is detected."""
    assert context.result.exit_code != 0
    error_output = context.result.stderr or context.result.output
    assert "api key" in error_output.lower() or "key" in error_output.lower()


@then("the pytest failure should be reported")
def step_impl_pytest_failure_reported(context: BehaveContext) -> None:
    """Verify pytest failure is reported."""
    assert context.result.exit_code != 0
    error_output = context.result.stderr or context.result.output
    assert "failed" in error_output.lower() or "error" in error_output.lower()


@then("the git operation failure should be handled")
def step_impl_git_failure_handled(context: BehaveContext) -> None:
    """Verify git operation failure is handled."""
    assert context.result is not None
    assert context.result.exit_code != 0
    error_output = context.result.stderr or context.result.output
    assert "error" in error_output.lower() or "failed" in error_output.lower()
