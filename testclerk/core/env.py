import os

from testclerk.core.constants import Environment
from testclerk.core.errors import TestClerkEnvironmentError


def load_api_key() -> str:
    """Load the API key from the environment.

    Raises:
        TestClerkEnvironmentError: If the API key env variable not set

    Returns:
        str: LLM API key
    """
    key = os.environ.get(Environment.API_KEY, None)
    if not key:
        raise TestClerkEnvironmentError(
            message=f"{Environment.API_KEY} environment variable is not set",
            help_text=f"Set {Environment.API_KEY} and try again",
        )
    return key
