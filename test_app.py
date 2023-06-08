from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_websocket_message_format():
    with client.websocket_connect("/ws") as websocket:
        message = {"message": "Test Message"}
        websocket.send_json(message)
        response = websocket.receive_json()
        assert isinstance(response, dict)
        assert "id" in response
        assert "text" in response


def test_websocket_send_receive():
    with client.websocket_connect("/ws") as websocket:
        messages = ["Hello", "World", "Test"]
        for message in messages:
            websocket.send_json({"message": message})
            response = websocket.receive_json()
            assert "id" in response
            assert response["text"] == message