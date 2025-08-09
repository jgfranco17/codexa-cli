"""
Type stubs for testclerk module.
Provides type hints for better IDE support and code quality.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union


# Type stubs for testclerk.main
class CLI:
    """Type stub for the main CLI object."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the CLI."""
        return None


# Type stubs for testclerk.client.accessor
class RemoteAIAccessor:
    """Type stub for RemoteAIAccessor class."""

    def __init__(
        self,
        api_key: str,
        prompt: str,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "deepseek/deepseek-r1:free",
    ) -> None:
        pass

    @property
    def setup_prompt(self) -> str:
        """Return the setup prompt."""
        return ""

    def make_request(self, message: str, timeout: float = 60.0) -> str:
        """Make a request to the LLM API."""
        return ""


class ReportScanner(RemoteAIAccessor):
    """Type stub for ReportScanner class."""

    def __init__(self, api_key: str) -> None:
        pass

    def analyze_tests(self, test_output: str, timeout: float = 60.0) -> str:
        """Read the test execution output and generate a report."""
        return ""


class RepoAnalyzer(RemoteAIAccessor):
    """Type stub for RepoAnalyzer class."""

    def __init__(self, api_key: str) -> None:
        pass

    def compare_diff(self, diff: str, timeout: float = 60.0) -> str:
        """Analyze git diff and provide test recommendations."""
        return ""


# Type stubs for testclerk.client.executor
class TestcaseMetadata:
    """Type stub for TestcaseMetadata class."""

    def __init__(
        self,
        node_id: str,
        name: str,
        file: str,
        line_number: int,
        keywords: List[str],
        module: Optional[str] = None,
        cls: Optional[str] = None,
        function: Optional[str] = None,
    ) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary map structure."""
        return {}


class TestExecutor:
    """Type stub for TestExecutor class."""

    def __init__(self, test_ids: List[str]) -> None:
        pass

    def run(self, verbose: bool = False) -> tuple[int, str, str]:
        """Run the Pytest tests located at the specified path."""
        return (0, "", "")

    def collect_all_tests(self) -> List[str]:
        """Collect all available tests."""
        return []

    def get_structured_test_tree(self) -> Dict[str, Any]:
        """Get structured test tree."""
        return {}


# Type stubs for testclerk.core.env
def load_api_key() -> str:
    """Load API key from environment or configuration."""
    return ""


# Type stubs for testclerk.core.errors
class TestClerkError(Exception):
    """Base exception for TestClerk errors."""

    pass


class TestClerkAccessorError(TestClerkError):
    """Exception for accessor-related errors."""

    pass


class TestClerkInputError(TestClerkError):
    """Exception for input-related errors."""

    pass


class TestClerkOutputError(TestClerkError):
    """Exception for output-related errors."""

    pass


# Type stubs for testclerk.client.versioning
def compare_git_diff(ref_branch: str, directory: str) -> str:
    """Compare git diff between current branch and reference branch."""
    return ""


# Type stubs for testclerk.core.output
class ColorHandler:
    """Type stub for ColorHandler class."""

    def __init__(self) -> None:
        pass

    def setLevel(self, level: int) -> None:
        """Set the log level."""
        pass

    def setFormatter(self, formatter: Any) -> None:
        """Set the formatter."""
        pass


# Type stubs for testclerk.core.handler
class CliHandler:
    """Type stub for CliHandler class."""

    def __init__(self) -> None:
        pass


# Type aliases for commonly used types
TestMap = Dict[str, Dict[str, List[str]]]
CLIResult = tuple[int, str, str]  # exit_code, stdout, stderr
