from typing import List, Optional

from _pytest.config import get_config
from _pytest.main import Session


def collect_all_tests(paths: Optional[List[str]] = None) -> List[str]:
    """Collect all available Pytest node IDs.

    Args:
        paths (List[str], optional): List of base paths, defaults to None.

    Returns:
        List[str]: List of executable node IDs
    """
    config = get_config()
    args = paths if paths else []
    config.args = args
    config._initini(args)
    config.parse(args)
    session = Session.from_config(config)
    session.perform_collect()
    return [item.nodeid for item in session.items]
