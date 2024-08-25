import pytest
from unittest.mock import patch, Mock
from src.adapter.slack_adapter import SlackAdapter

@pytest.fixture
def slack_adapter():
    return SlackAdapter(logger=Mock())

@patch('src.adapter.slack_adapter.requests.post')
def test_create_channel_success(mock_post, slack_adapter):
    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "channel": {
            "id": "C12345678"
        }
    }
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    response = slack_adapter.create_channel("test-channel", False)

    assert response["status_code"] == 200
    assert response["channel"]["id"] == "C12345678"

@patch('src.adapter.slack_adapter.requests.post')
def test_create_channel_error(mock_post, slack_adapter):
    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": False,
        "error": "channel_not_found"
    }
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    response = slack_adapter.create_channel("test-channel", False)

    assert response["status_code"] == 400
    assert response["error"] == "HTTP error occurred: channel_not_found"

@patch('src.adapter.slack_adapter.requests.post')
def test_request_exception(mock_post, slack_adapter):
    mock_post.side_effect = Exception("Request error")

    response = slack_adapter.create_channel("test-channel", False)

    assert response["status_code"] == 500
    assert "Request error occurred" in response["error"]
