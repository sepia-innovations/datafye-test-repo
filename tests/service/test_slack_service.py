import pytest
from src.service.slack_service import SlackService
from src.models.create_channel_request import CreateChannelRequest
from unittest.mock import MagicMock

@pytest.fixture
def slack_service():
    return SlackService(logger=MagicMock())

def test_create_channel_valid(slack_service):
    slack_service.slack_core.create_channel = MagicMock(return_value={
        "status_code": 200,
        "channel_id": "C12345678",
        "message": "Channel with name \"test-channel\" created successfully."
    })
    
    request = CreateChannelRequest(channel_name="test-channel", is_private=False)
    status_code, response = slack_service.create_channel(request)
    
    assert status_code == 200
    assert response["channel_id"] == "C12345678"
    assert response["message"] == "Channel with name \"test-channel\" created successfully."

def test_create_channel_invalid(slack_service):
    slack_service.slack_core.create_channel = MagicMock(return_value={
        "status_code": 400,
        "error": "Invalid Request. Channel name is missing."
    })
    
    request = CreateChannelRequest(channel_name="", is_private=False)
    status_code, response = slack_service.create_channel(request)
    
    assert status_code == 400
    assert "Invalid Request. Channel name is missing." in response["error"]
