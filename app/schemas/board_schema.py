from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BoardCreate(BaseModel):
    room_id: Optional[int]
    board_name: str
    ble_name: Optional[str]
    mac_address: str
    firmware_version: Optional[str]


class BoardOut(BaseModel):
    id: int
    room_id: Optional[int]
    board_name: str
    ble_name: Optional[str]
    mac_address: str
    firmware_version: Optional[str]
    online_status: Optional[bool]
    last_seen: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
