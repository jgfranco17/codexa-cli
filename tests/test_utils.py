from pytest import MonkeyPatch, raises

from codexa.core.env import load_api_key
from codexa.core.errors import CodexaEnvironmentError


def test_load_api_key_success(monkeypatch: MonkeyPatch):
    """Test that the API key is loaded correctly."""
    expected_key = "my-secret-api-key"
    monkeypatch.setenv("TESTCLERK_API_KEY", expected_key)
    found_key = load_api_key()
    assert found_key == expected_key


def test_load_api_key_not_set_failure(monkeypatch: MonkeyPatch):
    """Test that the API key is loaded correctly."""
    monkeypatch.delenv("TESTCLERK_API_KEY", raising=False)
    with raises(CodexaEnvironmentError):
        _ = load_api_key()
