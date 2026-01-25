from datetime import date
from typing import Optional, ClassVar
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    age: Optional[int] = Field(gt=-1, lt=100, default=None)
    email: Optional[EmailStr] = Field(default=None)
    birthday: Optional[date] = Field(default=None)
    name: Optional[str] = Field(default=None, min_length=1)
    avatar: Optional[str] = Field(default=None, min_length=3)

class UserCreate(UserBase):
    age: int = Field(gt=0, lt=100)
    email: EmailStr = Field()
    birthday: date = Field()
    name: str = Field(min_length=1)
    password: str = Field(min_length=6)
    avatar: Optional[str] = Field(default=None, min_length=3)

    model_config: ClassVar = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "password": "123456",
                "name": "user1",
                "avatar": "https://i.imgur.com/4M34hi2.png",
                "age": 18,
                "email": "user1@email.com",
                "birthday": "2003-01-01"
            }
        }
    }
    
class UserRead(BaseModel):
    id: int

class UserPasswordUpdate(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)

class UserUpdateResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

class UserinforResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)