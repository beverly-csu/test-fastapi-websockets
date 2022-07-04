from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()


@app.get('/')
async def root():
    with open('user.html', 'r', encoding='utf-8') as html_file:
        html = html_file.read()
    return HTMLResponse(html)


@app.websocket('/list')
async def websocket_list(websocket: WebSocket):
    await websocket.accept()
    count = 0
    try:
        while True:
            data = await websocket.receive_json()
            if 'item' in data.keys():
                count += 1
                await websocket.send_json({'count': count, 'item': data['item']})  
    except WebSocketDisconnect:
        print(f"Total messages were sent: {count}")
