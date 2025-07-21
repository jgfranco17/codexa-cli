import logging
import os
from pathlib import Path
from typing import Optional

import click

from testclerk.client.accessor import RepoAnalyzer
from testclerk.client.versioning import compare_git_diff
from testclerk.core.env import load_api_key
from testclerk.core.errors import TestClerkInputError, TestClerkOutputError

logger = logging.getLogger(__name__)


@click.command("compare")
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True, path_type=str),
    required=False,
    default=os.getcwd(),
    help="Output file with generated code",
)
@click.option(
    "--ref-branch",
    "ref_branch",
    "-r",
    type=str,
    required=False,
    default="os.getcwd()",
    help="Remote branch to compare against",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress test execution shell output",
)
@click.option(
    "--output",
    "output",
    "-o",
    type=click.Path(exists=False, dir_okay=False, resolve_path=True, path_type=Path),
    required=False,
    default=Path(Path.cwd(), "report.md"),
    help="Output file with generated code",
)
def compare_command(
    directory: str, ref_branch: str, quiet: bool, output: Optional[Path]
) -> None:
    """Generate smart analysis from diff comparison.."""
    if output is not None and output.suffix != ".md":
        raise TestClerkInputError(
            message=f"Output file must be a Markdown file, got {output.suffix}",
            help_text=f"Rename the output file to a {output.stem}.md",
        )
    key = load_api_key()
    diff = compare_git_diff(ref_branch, directory)
    logger.info("Forwarding git diff to LLM")
    analyzer = RepoAnalyzer(key)
    assessment = analyzer.compare_diff(diff)

    click.secho(
        f"[!] Recommendations for tests: {directory}",
        fg="green",
        bold=True,
    )
    if not quiet:
        click.echo(assessment)

    if output is not None:
        output.write_text(assessment)
        logger.info(f"Diff report generated: {output.absolute()}")
