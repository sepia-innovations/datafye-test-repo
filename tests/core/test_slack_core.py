from unittest.mock import MagicMock
import pytest
from src.core.slack_core import SlackCore

@pytest.fixture
def slack_core():
    return SlackCore(logger=MagicMock())

def test_handle_api_response_success(slack_core):
    response = {
        "ok": True,
        "channel": {
            "id": "C12345678"
        }
    }
    result = slack_core.handle_api_response(response, "Success", "Failure")
    assert result["status_code"] == 200
    assert result["channel_id"] == "C12345678"
    assert result["message"] == "Success"

def test_handle_api_response_error(slack_core):
    response = {
        "ok": False,
        "error": "channel_not_found"
    }
    result = slack_core.handle_api_response(response, "Success", "Failure")
    assert result["status_code"] == 400
    assert "The channel does not exist." in result["error"]
