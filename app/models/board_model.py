from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    board_name = Column(String(120), nullable=False)
    ble_name = Column(String(120), nullable=True)
    mac_address = Column(String(60), unique=True, nullable=False, index=True)
    firmware_version = Column(String(60), nullable=True)
    online_status = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", backref="boards")
