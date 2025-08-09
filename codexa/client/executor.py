import io
import logging
from collections import defaultdict
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest
from _pytest.reports import CollectReport

logger = logging.getLogger(__name__)


TestMap = Dict[str, Dict[str, List[str]]]


@dataclass(frozen=True)
class TestcaseMetadata:
    """Test case metadata model."""

    node_id: str
    name: str
    file: str
    line_number: int
    keywords: List[str]
    module: Optional[str] = None
    cls: Optional[str] = None
    function: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary map structure."""
        return asdict(self)


class TestExecutor:
    """Class for executing tests."""

    def __init__(self, test_ids: List[str]):
        self.__test_ids = test_ids

    def run(self, verbose: bool = False) -> Tuple[int, str, str]:
        """Run the Pytest tests located at the specified path.

        Args:
            path (str): _description_

        Returns:
            Tuple[str, str, int]: _description_
        """
        stdout = io.StringIO()
        stderr = io.StringIO()

        pytest_base_args = []
        if verbose:
            pytest_base_args.append("-vv")

        # Redirect both stdout and stderr during the test run
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = pytest.main([*pytest_base_args, *self.__test_ids])

        # Retrieve output
        shell_output = stdout.getvalue()
        error_output = stderr.getvalue()

        return exit_code, shell_output, error_output

    @staticmethod
    def __collect_ids(paths: List[str]) -> List[TestcaseMetadata]:
        args = ["--collect-only", "-q", "-p", "no:warnings"]
        if paths:
            args.extend([str(Path(p).resolve()) for p in paths])

        # Collect test data
        collected = []

        class CollectorPlugin:
            def pytest_collectreport(self, report: CollectReport):
                if report.failed:
                    logger.error(report.longrepr)

            def pytest_itemcollected(self, item: Any):
                file, line_number, _ = item.location
                entry = TestcaseMetadata(
                    node_id=item.nodeid,
                    name=item.name,
                    file=file,
                    line_number=line_number,
                    keywords=list(item.keywords),
                    module=item.module.__name__ if item.module else None,
                    cls=item.cls.__name__ if item.cls else None,
                    function=getattr(item.function, "__name__", None),
                )
                collected.append(entry)

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            pytest.main(args, plugins=[CollectorPlugin()])
        return collected

    def collect_all_tests(self) -> List[str]:
        """Collect all available Pytest node IDs.

        Args:
            paths (List[str], optional): List of base paths, defaults to None.

        Returns:
            List[str]: List of executable node IDs
        """
        entries = self.__collect_ids(self.__test_ids)
        return [entry.node_id for entry in entries]

    def get_structured_test_tree(self) -> Dict[str, Any]:
        """Generate a mapping of available tests.

        Args:
            paths (List[str], optional): List of base paths, defaults to None.

        Returns:
            TestTree: Test entries map
        """
        entries = self.__collect_ids(self.__test_ids)
        test_map = defaultdict(lambda: defaultdict(list))

        for entry in entries:
            module_path = entry.file
            class_name = entry.cls
            func_name = entry.name

            test_map[module_path][class_name].append(func_name)

        return test_map
