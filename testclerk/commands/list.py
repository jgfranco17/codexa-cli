import json
import logging
import os
from pathlib import Path

import click

from testclerk.client.accessor import ReportScanner
from testclerk.client.executor import TestExecutor
from testclerk.core.env import load_api_key
from testclerk.core.errors import TestClerkGenerationError, TestClerkInputError

logger = logging.getLogger(__name__)


@click.command("list")
@click.option(
    "--base-dir",
    "base_dir",
    "-b",
    type=click.Path(exists=False, file_okay=False, path_type=Path),
    required=False,
    default=Path(Path.cwd(), "tests"),
    help="Base directory of tests",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Print the test list as JSON map",
)
def list_command(base_dir: Path, as_json: bool) -> None:
    """List all available tests."""
    rendered_output = ""
    base_path = [str(base_dir)]
    executor = TestExecutor(base_path)
    if as_json:
        logger.debug("Generating JSON map of all tests")
        test_map = executor.get_structured_test_tree()
        rendered_output = json.dumps(
            test_map, indent=2, sort_keys=True, ensure_ascii=False
        )
    else:
        logger.debug("Generating list of all tests")
        numbered_list = [
            f"{index}. {entry}"
            for index, entry in enumerate(executor.collect_all_tests(), start=1)
        ]
        rendered_output = "\n".join(numbered_list)
    click.echo(rendered_output)
