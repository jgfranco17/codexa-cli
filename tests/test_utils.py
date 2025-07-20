from pytest import MonkeyPatch, raises

from testclerk.core.env import load_api_key
from testclerk.core.errors import TestClerkEnvironmentError


def test_load_api_key_success(monkeypatch: MonkeyPatch) -> None:
    """Test that the API key is loaded correctly."""
    expected_key = "my-secret-api-key"
    monkeypatch.setenv("TESTCLERK_API_KEY", expected_key)
    found_key = load_api_key()
    assert found_key == expected_key


def test_load_api_key_not_set_failure(monkeypatch: MonkeyPatch) -> None:
    """Test that the API key is loaded correctly."""
    monkeypatch.delenv("TESTCLERK_API_KEY", raising=False)
    with raises(TestClerkEnvironmentError):
        _ = load_api_key()
