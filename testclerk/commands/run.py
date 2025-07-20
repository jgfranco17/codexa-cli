import logging
from pathlib import Path
from typing import List

import click

from testclerk.client.accessor import ReportScanner
from testclerk.client.executor import TestExecutor
from testclerk.core.env import load_api_key
from testclerk.core.errors import TestClerkAccessorError, TestClerkInputError

logger = logging.getLogger(__name__)


@click.command("run")
@click.argument("test_ids", nargs=-1)
@click.option(
    "--output",
    "output",
    "-o",
    type=click.Path(exists=False, dir_okay=False, resolve_path=True, path_type=Path),
    required=False,
    default=Path(Path.cwd(), "report.md"),
    help="Output file with generated code",
)
@click.option(
    "--quiet",
    "quiet",
    "-q",
    is_flag=True,
    help="Suppress test execution shell output",
)
def run_command(test_ids: List[str], output: Path, quiet: bool) -> None:
    """Analyze the contents of a file for testing."""
    if output.suffix != ".md":
        raise TestClerkInputError(
            message=f"Output file must be a Markdown file, got {output.suffix}",
            help_text=f"Rename the output file to a {output.stem}.md",
        )
    key = load_api_key()
    client = ReportScanner(key)
    if not test_ids:
        logger.info("No test IDs provided, running all tests")

    executor = TestExecutor(test_ids)
    exit_code, shell_output, error_output = executor.run(verbose=not quiet)
    if not quiet:
        click.echo(shell_output)
        click.echo(error_output)
    if exit_code != 0:
        raise TestClerkAccessorError(
            message=f"Failed to generate tests: {error_output}",
            help_text=f"Please check the output for more information",
        )

    logger.debug(f"Test execution complete, proceeding to results analysis")
    response = client.analyze_tests(shell_output)
    try:
        with open(output, "w") as f:
            f.write(response)
    except IOError as e:
        raise TestClerkAccessorError(
            message=f"Failed to generate test file: {e}",
        )

    click.secho(
        f"\n[!] Test summary generated! Report file: {output}",
        fg="green",
        bold=True,
    )
