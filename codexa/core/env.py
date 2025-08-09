import os

from codexa.core.constants import Environment
from codexa.core.errors import CodexaEnvironmentError


def load_api_key() -> str:
    """Load the API key from the environment.

    Raises:
        CodexaEnvironmentError: If the API key env variable not set

    Returns:
        str: LLM API key
    """
    key = os.environ.get(Environment.API_KEY, None)
    if not key:
        raise CodexaEnvironmentError(
            message=f"{Environment.API_KEY} environment variable is not set",
            help_text=f"Set {Environment.API_KEY} and try again",
        )
    return key
