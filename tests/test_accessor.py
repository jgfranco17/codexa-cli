import pytest

from testclerk.client.accessor import RemoteAIAccessor
from testclerk.core.errors import TestClerkAccessorError


def test_accessor_init_ok():
    accessor = RemoteAIAccessor(api_key="dummy-key", prompt="dummy-prompt")
    assert accessor.setup_prompt == "dummy-prompt"


def test_accessor_init_no_api_key_fail():
    with pytest.raises(TestClerkAccessorError):
        _ = RemoteAIAccessor(api_key="", prompt="dummy-prompt")


def test_accessor_init_no_prompt_fail():
    with pytest.raises(TestClerkAccessorError):
        _ = RemoteAIAccessor(api_key="dummy-key", prompt="")
