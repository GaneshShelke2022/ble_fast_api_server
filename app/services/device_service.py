from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.device_model import Device


async def list_devices(db: AsyncSession):
    q = await db.execute(select(Device))
    return q.scalars().all()


async def create_device(db: AsyncSession, **data):
    d = Device(**data)
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d


async def update_device(db: AsyncSession, device_id: int, **changes):
    q = await db.execute(select(Device).where(Device.id == device_id))
    d = q.scalars().first()
    if not d:
        return None
    for k, v in changes.items():
        setattr(d, k, v)
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d


async def delete_device(db: AsyncSession, device_id: int):
    q = await db.execute(select(Device).where(Device.id == device_id))
    d = q.scalars().first()
    if not d:
        return False
    await db.delete(d)
    await db.commit()
    return True
