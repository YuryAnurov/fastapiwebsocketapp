from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from typing import Dict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# словарь для хранения подключенных клиентов и их счетчиков
clients: Dict[WebSocket, int] = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # получаем значение счетчика клиента, для нового клиента устанавливаем 1
    counter = clients.get(websocket, 1)
    # При перезагрузке страницы отправляем message клиенту
    if counter == 1:
        await websocket.send_json({"reset": True})
        
    try:
        while True:
            data = await websocket.receive_json()
            message = {"id": counter, "text": data["message"]}
            await websocket.send_json(message)
            counter += 1
            clients[websocket] = counter  # обновляем счетчик клиента
    except WebSocketDisconnect:
        pass


@app.on_event("shutdown")
async def shutdown_event():
    clients.clear()  # При остановке сервера очищаем словарик клиентов