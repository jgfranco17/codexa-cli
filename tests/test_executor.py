from pathlib import Path

from testclerk.client.executor import TestExecutor


def test_executor_collect_all_tests(tmp_path: Path, mock_pytest_file: Path) -> None:
    executor = TestExecutor([str(tmp_path)])
    results = executor.collect_all_tests()
    assert results == [
        "test_example.py::test_foo",
        "test_example.py::TestBar::test_bar",
    ]
