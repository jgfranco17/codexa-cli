from unittest.mock import MagicMock

import pytest

from codexa.client.accessor import RemoteAIAccessor, ReportScanner
from codexa.core.errors import CodexaAccessorError


def test_accessor_init_ok():
    accessor = RemoteAIAccessor(api_key="dummy-key", prompt="dummy-prompt")
    assert accessor.setup_prompt == "dummy-prompt"


@pytest.mark.parametrize(
    "mock_api_key, mock_prompt",
    [
        ("", "Some valid prompt"),
        ("valid-key", ""),
    ],
)
def test_accessor_init_fail_missing_input(mock_api_key: str, mock_prompt: str):
    with pytest.raises(CodexaAccessorError):
        _ = RemoteAIAccessor(api_key=mock_api_key, prompt=mock_prompt)


def test_analyze_tests_successful(mock_openai_client: MagicMock):
    mock_client_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="## Summary\n- 2 passed, 1 failed"))
    ]
    mock_client_instance.chat.completions.create.return_value = mock_response
    mock_openai_client.return_value = mock_client_instance

    generator = ReportScanner(api_key="dummy-key")
    report = generator.analyze_tests(test_output="1 failed, 2 passed")
    assert "## Summary" in report
    mock_client_instance.chat.completions.create.assert_called_once()


def test_analyze_tests_create_failure(mock_openai_client: MagicMock):
    mock_client_instance = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = None
    mock_choice.message.refusal = "Content policy triggered"
    mock_response.choices = [mock_choice]
    mock_client_instance.chat.completions.create.return_value = mock_response
    mock_openai_client.return_value = mock_client_instance

    generator = ReportScanner(api_key="dummy-key")
    with pytest.raises(CodexaAccessorError, match="Failed to generate code"):
        _ = generator.analyze_tests(test_output="Some mock report output")
    mock_client_instance.chat.completions.create.assert_called_once()
