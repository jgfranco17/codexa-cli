from tests.conftest import CommandRunner


def test_help_message_sane(runner: CommandRunner) -> None:
    """Test a sane basic help call."""
    result = runner.run_cli(["--help"])
    assert result.exit_code == 0
