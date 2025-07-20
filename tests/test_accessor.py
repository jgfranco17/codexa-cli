import pytest

from testclerk.client.accessor import RemoteAIAccessor


def test_accessor_init_ok() -> None:
    accessor = RemoteAIAccessor(api_key="dummy-key", prompt="dummy-prompt")
    assert accessor.setup_prompt == "dummy-prompt"


def test_accessor_init_no_api_key_fail() -> None:
    with pytest.raises(ValueError):
        _ = RemoteAIAccessor(api_key="", prompt="dummy-prompt")


def test_accessor_init_no_prompt_fail() -> None:
    with pytest.raises(ValueError):
        _ = RemoteAIAccessor(api_key="dummy-key", prompt="")
