from schemas import users as UserSchema
from database.generic import get_db
from model.user import User as UserModel
from sqlalchemy import select, update, delete
from fastapi import Depends
from api.depends import check_user_id

async def get_users_infor(keyword: str = None, last: int = 0, limit: int = 50, db = Depends(get_db)):
    stmt = select(UserModel)
    if keyword:
        stmt = stmt.where(UserModel.name.like(f"%{keyword}%"))
    stmt = stmt.offset(last).limit(limit)
    result = await db.scalars(stmt).all()
    return result

async def get_user_by_id(user_id: int, db = Depends(get_db)):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.scalar(stmt)
    return result

async def create_users(new_user: UserSchema.UserCreate, db = Depends(get_db)):
    user = UserModel(**new_user.model_dump())

    stmt = select(UserModel.id).where(UserModel.email == new_user.email)
    result = await db.scalar(stmt)
    if result is not None:
        return None

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def delete_users(current_user:UserModel = Depends(check_user_id), db = Depends(get_db)):
    stmt = delete(UserModel).where(UserModel.id == current_user.id)
    await db.execute(stmt)
    await db.commit()
    return {"message": "User deleted successfully"}

async def update_user_optional(user_update: UserSchema.UserBase, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    stmt = update(UserModel).where(UserModel.id == current_user.id).values(**user_update.model_dump(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    stmt = select(UserModel).where(UserModel.id == current_user.id)
    result = await db.scalar(stmt)
    return result
        
async def change_password(update_info: UserSchema.UserPasswordUpdate, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    if current_user.password != update_info.old_password:
        raise None

    stmt = update(UserModel).where(UserModel.id == current_user.id).values(password=update_info.new_password)
    await db.execute(stmt)
    await db.commit()
    return {"message": "Password updated successfully"}
