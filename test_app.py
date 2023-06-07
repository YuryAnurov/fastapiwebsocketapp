from fastapi.testclient import TestClient
from main import app

def test_websocket_endpoint():
    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        # тестируем первое сообщение с сервера
        response = websocket.receive_json()
        assert "reset" in response

        # тестируем отправку сообщений и получение ответов
        messages = ["Hello", "World", "Test"]
        for message in messages:
            websocket.send_json({"message": message})
            response = websocket.receive_json()
            assert "id" in response
            assert response["text"] == message
