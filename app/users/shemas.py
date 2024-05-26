from pydantic import BaseModel, EmailStr
from typing import Optional


class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    role: str

    class Config:
        from_attributes = True


class SUserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str


class SUserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None
