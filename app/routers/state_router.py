from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..database import get_async_session
from ..services.websocket_service import save_state
from ..schemas.state_schema import StateCreate, StateOut
from ..utils.response import success_response, error_response
from ..websocket.connection_manager import ConnectionManager
from ..websocket.connection_manager import ConnectionManager
from ..websocket.connection_manager import ConnectionManager
from ..websocket.connection_manager import ConnectionManager
from ..websocket.connection_manager import ConnectionManager

router = APIRouter(prefix="/states", tags=["states"])

# simple module-level manager for broadcasting
from ..websocket.connection_manager import ConnectionManager as _CM
manager = _CM()


@router.get("")
async def get_states(db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    # returns last states - simplified
    q = await db.execute("SELECT * FROM device_states ORDER BY updated_at DESC LIMIT 100")
    rows = q.fetchall()
    return rows


@router.post("")
async def post_state(data: StateCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    try:
        ds = await save_state(db, data.device_id, data.state, data.brightness)
        payload = {"device_id": data.device_id, "state": data.state, "brightness": data.brightness, "mesh_address": data.mesh_address}
        # broadcast to websocket clients
        await manager.broadcast({"type": "state_update", "payload": payload})
        return success_response("State saved", StateOut.from_orm(ds).dict())
    except Exception as e:
        return error_response(str(e))
