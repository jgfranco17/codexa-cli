import os

from testclerk.core.constants import Environment
from testclerk.core.errors import TestClerkEnvironmentError


def load_api_key() -> str:
    key = os.environ.get(Environment.API_KEY, None)
    if not key:
        raise TestClerkEnvironmentError(
            message=f"{Environment.API_KEY} environment variable is not set",
            help_text=f"Set {Environment.API_KEY} and try again",
        )
    return key
