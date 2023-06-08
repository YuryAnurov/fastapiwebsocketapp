from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

app = FastAPI(websocket_origin='127.0.0.1')
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket.accept()
    counter = 1
    try:
        while True:
            data = await websocket.receive_json()
            message = {"id": counter, "text": data["message"]}
            await websocket.send_json(message)
            counter += 1
    except WebSocketDisconnect:
        pass