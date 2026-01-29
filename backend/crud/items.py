from schemas import users as UserSchema
from database.generic import get_db
from model.user import User as UserModel
from sqlalchemy import select, update, delete
from fastapi import Depends
from api.depends import check_user_id

def get_users_infor(db = Depends(get_db)):
    stmt = select(UserModel)
    result = db.scalars(stmt).all()
    return result

def get_user_by_id(user_id: int, db = Depends(get_db)):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = db.scalar(stmt)
    return result

def create_users(new_user: UserSchema.UserCreate, db = Depends(get_db)):
    user = UserModel(**new_user.model_dump())

    stmt = select(UserModel.id).where(UserModel.email == new_user.email)
    result = db.scalar(stmt)
    if result is not None:
        return None

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_users(current_user:UserModel = Depends(check_user_id), db = Depends(get_db)):
    stmt = delete(UserModel).where(UserModel.id == current_user.id)
    db.execute(stmt)
    db.commit()
    return {"message": "User deleted successfully"}

def update_user_optional(user_update: UserSchema.UserBase, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    stmt = update(UserModel).where(UserModel.id == current_user.id).values(**user_update.model_dump(exclude_unset=True))
    db.execute(stmt)
    db.commit()
    stmt = select(UserModel).where(UserModel.id == current_user.id)
    result = db.scalar(stmt)
    return result
        
def change_password(update_info: UserSchema.UserPasswordUpdate, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    if current_user.password != update_info.old_password:
        raise None

    stmt = update(UserModel).where(UserModel.id == current_user.id).values(password=update_info.new_password)
    db.execute(stmt)
    db.commit()
    return {"message": "Password updated successfully"}
