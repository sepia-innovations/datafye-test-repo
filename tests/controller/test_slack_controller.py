import json
from fastapi.testclient import TestClient
from main import app
from tests.mocks.create_channel_request_valid.json import valid_request
from tests.mocks.create_channel_request_invalid.json import invalid_request

client = TestClient(app)

def test_create_channel_valid():
    response = client.post("/slack/create_channel", data=json.dumps(valid_request), headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.json()["channel_id"] == "C12345678"

def test_create_channel_invalid():
    response = client.post("/slack/create_channel", data=json.dumps(invalid_request), headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert "Invalid Request. Channel name is missing." in response.json()["error"]
