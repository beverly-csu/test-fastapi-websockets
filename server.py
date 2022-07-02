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
    item_list = list()
    try:
        while True:
            data = await websocket.receive_json()
            if 'item' in data.keys():
                item_list.append(data['item'])
                await websocket.send_json({'count': len(item_list), 'item': data['item']})  
    except WebSocketDisconnect:
        print(item_list)
        del item_list