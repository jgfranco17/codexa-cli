from unittest.mock import MagicMock

from testclerk.client.accessor import ReportScanner


def test_analyze_tests_successful(mock_openai_client: MagicMock):
    """Test that a valid LLM response returns correct report."""
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
