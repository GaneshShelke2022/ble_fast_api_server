from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoomCreate(BaseModel):
    room_name: str
    room_icon: Optional[str]


class RoomOut(BaseModel):
    id: int
    room_name: str
    room_icon: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
