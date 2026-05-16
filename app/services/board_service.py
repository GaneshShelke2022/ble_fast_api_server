from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.board_model import Board


async def list_boards(db: AsyncSession):
    q = await db.execute(select(Board))
    return q.scalars().all()


async def create_board(db: AsyncSession, **data):
    # prevent duplicate mac_address
    q = await db.execute(select(Board).where(Board.mac_address == data.get("mac_address")))
    existing = q.scalars().first()
    if existing:
        return None, "Board already added"
    b = Board(**data)
    db.add(b)
    await db.commit()
    await db.refresh(b)
    return b, None


async def update_board(db: AsyncSession, board_id: int, **changes):
    q = await db.execute(select(Board).where(Board.id == board_id))
    b = q.scalars().first()
    if not b:
        return None
    for k, v in changes.items():
        setattr(b, k, v)
    db.add(b)
    await db.commit()
    await db.refresh(b)
    return b


async def delete_board(db: AsyncSession, board_id: int):
    q = await db.execute(select(Board).where(Board.id == board_id))
    b = q.scalars().first()
    if not b:
        return False
    await db.delete(b)
    await db.commit()
    return True
