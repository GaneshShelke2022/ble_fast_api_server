from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    board_id: int
    device_name: str
    device_type: Optional[str] = "lamp"
    channel_no: Optional[int]
    mesh_address: int
    icon: Optional[str]


class DeviceOut(BaseModel):
    id: int
    board_id: int
    device_name: str
    device_type: str
    channel_no: Optional[int]
    mesh_address: int
    icon: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
