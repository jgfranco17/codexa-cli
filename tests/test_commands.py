from tests.tools import CommandRunner, verify_cli_output


class TestBaseCommands:
    """Test the base CLI commands."""

    def test_help_message_ok(self, runner: CommandRunner) -> None:
        result = runner.run_cli(["--help"])
        assert result.exit_code == 0


class TestRunCommand:
    """Test the execution and report generation."""

    def test_invalid_report_path(self, runner: CommandRunner) -> None:
        result = runner.run_cli(["run", "--output", "report.txt"])
        verify_cli_output(
            result, 2, expected_stderr="Output file must be a Markdown file, got .txt"
        )
