from datetime import date
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id: int

class UserCreate(UserBase):
    age: int
    email: str
    birthday: date
    name: str
    password: str
    avatar: Optional[str]

class UserRead(UserBase):
    name: str
    email: str
    avatar: Optional[str]