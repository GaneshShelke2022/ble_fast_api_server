from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StateCreate(BaseModel):
    device_id: int
    state: int
    brightness: Optional[int]
    mesh_address: Optional[int]


class StateOut(BaseModel):
    id: int
    device_id: int
    state: int
    brightness: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
