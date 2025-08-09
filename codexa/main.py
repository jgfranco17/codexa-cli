import logging

import click
import colorama

from codexa import __version__
from codexa.commands.compare import compare_command
from codexa.commands.list import list_command
from codexa.commands.run import run_command
from codexa.core.handler import CliHandler
from codexa.core.output import ColorHandler

colorama.init(autoreset=True)


def __get_log_level(verbosity: int) -> int:
    levels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    return levels.get(verbosity, logging.DEBUG)


def __set_logger(level: int):
    logger = logging.getLogger(__package__)
    log_level = __get_log_level(level)
    logger.setLevel(log_level)
    handler = ColorHandler()
    handler.setLevel(log_level)

    timestamp_format = "[%(asctime)s][%(levelname)s] %(message)s"
    if log_level == logging.DEBUG:
        timestamp_format = "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(
        fmt=timestamp_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@click.group(cls=CliHandler)
@click.pass_context
@click.version_option(version=__version__)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity. Use multiple times for more detail (e.g., -vv for debug).",
)
def cli(context: click.Context, verbose: int):
    """Codexa: CLI tool for test automation assistance."""
    __set_logger(verbose)
    context.ensure_object(dict)


cli.add_command(run_command)
cli.add_command(list_command)
cli.add_command(compare_command)
