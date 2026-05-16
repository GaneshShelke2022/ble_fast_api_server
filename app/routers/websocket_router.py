from fastapi import APIRouter, WebSocket, Depends
from fastapi import WebSocketDisconnect
from ..websocket.connection_manager import ConnectionManager
from ..websocket.websocket_handler import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # simply forward to handler's broadcast
            await manager.broadcast({"type": "raw_message", "payload": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
