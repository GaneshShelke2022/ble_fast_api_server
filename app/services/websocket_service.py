from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.state_model import DeviceState


async def save_state(db: AsyncSession, device_id: int, state: int, brightness: int = None):
    # create a new state entry
    ds = DeviceState(device_id=device_id, state=state, brightness=brightness)
    db.add(ds)
    await db.commit()
    await db.refresh(ds)
    return ds
