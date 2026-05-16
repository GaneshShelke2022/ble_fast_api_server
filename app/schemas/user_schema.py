from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
