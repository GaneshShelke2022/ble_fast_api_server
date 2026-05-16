from fastapi import WebSocket, WebSocketDisconnect
from ..websocket.connection_manager import ConnectionManager
from ..services.websocket_service import save_state
from ..database import get_async_session
import json

manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # expecting JSON like {"a":4098, "s":1}
            try:
                payload = json.loads(data)
            except Exception:
                await manager.send_personal_message({"success": False, "message": "Invalid JSON"}, websocket)
                continue

            # broadcast to everyone
            await manager.broadcast({"type": "state_update", "payload": payload})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
