from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from ..models.room_model import Room


async def list_rooms(db: AsyncSession):
    q = await db.execute(select(Room))
    return q.scalars().all()


async def create_room(db: AsyncSession, room_name: str, room_icon: str = None):
    r = Room(room_name=room_name, room_icon=room_icon)
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r


async def update_room(db: AsyncSession, room_id: int, room_name: str = None, room_icon: str = None):
    q = await db.execute(select(Room).where(Room.id == room_id))
    r = q.scalars().first()
    if not r:
        return None
    if room_name:
        r.room_name = room_name
    if room_icon is not None:
        r.room_icon = room_icon
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r


async def delete_room(db: AsyncSession, room_id: int):
    q = await db.execute(select(Room).where(Room.id == room_id))
    r = q.scalars().first()
    if not r:
        return False
    await db.delete(r)
    await db.commit()
    return True
