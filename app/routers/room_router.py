from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..database import get_async_session
from ..services.room_service import list_rooms, create_room, update_room, delete_room
from ..schemas.room_schema import RoomCreate, RoomOut
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomOut])
async def get_rooms(db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    rooms = await list_rooms(db)
    return rooms


@router.post("")
async def add_room(data: RoomCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    try:
        r = await create_room(db, room_name=data.room_name, room_icon=data.room_icon)
        return success_response("Room added successfully", RoomOut.from_orm(r).dict())
    except Exception as e:
        return error_response(str(e))


@router.put("/{room_id}")
async def edit_room(room_id: int, data: RoomCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    r = await update_room(db, room_id, room_name=data.room_name, room_icon=data.room_icon)
    if not r:
        raise HTTPException(status_code=404, detail="Room not found")
    return success_response("Room updated", RoomOut.from_orm(r).dict())


@router.delete("/{room_id}")
async def remove_room(room_id: int, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    ok = await delete_room(db, room_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Room not found")
    return success_response("Room deleted", None)
