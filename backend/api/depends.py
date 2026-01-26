from typing import Optional
from sqlalchemy import select
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from model.user import User as UserModel
from database.generic import get_db
from fastapi import Header

def check_user_id(user_id: int, db: Session = Depends(get_db)):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = db.scalar(stmt)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

class PaginationParams:
    def __init__(self, keyword: Optional[str] = None, last: int = 0, limit: int = 50):
        self.keyword = keyword
        self.last = last
        self.limit = limit

def test_vertify_token(vertify_header: str = Header()):
    if vertify_header != "123":
        raise HTTPException(status_code=403, detail="Forbidden: access token invalid")
    return vertify_header