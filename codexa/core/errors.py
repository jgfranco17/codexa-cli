"""CLI exceptions."""

from typing import Final, Optional


class ExitCode:
    """Class for CLI Exit Codes."""

    SUCCESS: Final[int] = 0
    RUNTIME_ERROR: Final[int] = 1
    INPUT_ERROR: Final[int] = 2
    ENVIRONMENT_ERROR: Final[int] = 3
    EXECUTION__ERROR: Final[int] = 4
    ACCESS_ERROR: Final[int] = 5
    GENERATION_ERROR: Final[int] = 6
    OUTPUT_ERROR: Final[int] = 7


class CodexaBaseError(Exception):
    """A base CLI Error class.

    Contains a message, exit_code and help text show to the user

    exit_code should be a member of ExitCode
    """

    def __init__(self, message: str, exit_code: int, help_text: Optional[str]):
        """Init an CLI Error."""
        self.message = message
        self.exit_code = exit_code
        if help_text is None:
            help_text = "Help is available with --help. Use the -v flag to increase output verbosity."
        self.help_text = help_text
        super().__init__(self.message)


class CodexaRuntimeError(CodexaBaseError):
    """General CLI CLI Error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an CLI CLI Error."""
        self.message = message
        super().__init__(self.message, ExitCode.RUNTIME_ERROR, help_text)


class CodexaInputError(CodexaBaseError):
    """CLI user input error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an CLI Input Error."""
        self.message = message
        super().__init__(self.message, ExitCode.INPUT_ERROR, help_text)


class CodexaEnvironmentError(CodexaBaseError):
    """CLI environmnt error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an CLI Environment Error."""
        self.message = message
        super().__init__(self.message, ExitCode.ENVIRONMENT_ERROR, help_text)


class CodexaExecutionError(CodexaBaseError):
    """CLI test execution error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an CLI Generation Error."""
        self.message = message
        super().__init__(self.message, ExitCode.GENERATION_ERROR, help_text)


class CodexaAccessorError(CodexaBaseError):
    """CLI LLM generation error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an CLI Generation Error."""
        self.message = message
        super().__init__(self.message, ExitCode.GENERATION_ERROR, help_text)


class CodexaOutputError(CodexaBaseError):
    """CLI LLM generation error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an CLI Generation Error."""
        self.message = message
        super().__init__(self.message, ExitCode.GENERATION_ERROR, help_text)
