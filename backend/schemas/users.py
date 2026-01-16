from datetime import date
from typing import Optional, ClassVar
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    id: int

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
    

class UserRead(UserBase):
    name: str
    email: str
    avatar: Optional[str]