from datetime import date
from pydantic import BaseModel, validator

class User(BaseModel):
    id: int
    name: str
    birthday: date

    @validator('id')
    def id_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('id must be positive')
        return v

    @validator('name')
    def name_must_be_capitalized(cls, v):
        if v[0].islower():
            raise ValueError('name must be capitalized')
        return v

    @validator('birthday')
    def birthday_must_be_after_2000(cls, v):
        if v.year < 2000:
            raise ValueError('birthday must be after 2000')
        return v 

    def __str__(self):
        return f'User(id={self.id},name={self.name},birthday={self.birthday})'

    
    
try :
   User(id=1, name='John', birthday=date(2000, 1, 1))
except Exception as e:
    print(e)

try :
    User(id='str', name='John', birthday=date(2000, 1, 1))
except Exception as e:
    print(e)