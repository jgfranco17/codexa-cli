import logging
from dataclasses import dataclass
from typing import Final

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConsoleIcons:
    """Icons for the shell prints."""

    CHECK: Final[str] = "\u2713"
    CROSS: Final[str] = "\u2715"


@dataclass(frozen=True)
class Environment:
    """Environment variables for user configuration."""

    API_KEY: Final[str] = "TestClerk_API_KEY"
