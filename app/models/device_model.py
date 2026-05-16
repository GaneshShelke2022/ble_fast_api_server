from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    device_name = Column(String(120), nullable=False)
    device_type = Column(String(50), nullable=False, default="lamp")
    channel_no = Column(Integer, nullable=True)
    mesh_address = Column(Integer, nullable=False, index=True)
    icon = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    board = relationship("Board", backref="devices")
