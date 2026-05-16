from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(100), nullable=False)
    room_icon = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
