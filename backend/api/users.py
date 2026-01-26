from fastapi import APIRouter, HTTPException, status
from schemas import users as UserSchema
from database.generic import get_db
from model.user import User as UserModel
from sqlalchemy import select, update, delete
from fastapi import Depends
from api.depends import check_user_id
from typing import Annotated
from api.depends import PaginationParams
from api.depends import test_vertify_token

CommonPaginationParams = Annotated[PaginationParams, Depends()]

router = APIRouter(tags=["users"], prefix="/api/users", dependencies=[Depends(test_vertify_token)])
@router.get("/",
         response_model= list[UserSchema.UserinforResponse],
)
def get_users_infor(page_params: CommonPaginationParams, qry: str = None, db = Depends(get_db)):
    stmt = select(UserModel)
    result = db.scalars(stmt).all()
    return result

@router.get("/{user_id}", response_model= UserSchema.UserBase)
def get_user_by_id(user_id: int, qry: str = None, db = Depends(get_db)):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = db.scalar(stmt)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/",
          response_model=UserSchema.UserRead,
          status_code=status.HTTP_201_CREATED
)
def create_users(new_user: UserSchema.UserCreate, db = Depends(get_db)):
    user = UserModel(
        password = new_user.password,
        name = new_user.name,
        age = new_user.age,
        avatar = new_user.avatar,
        birthday = new_user.birthday,
        email = new_user.email
    )

    stmt = select(UserModel.id).where(UserModel.email == new_user.email)
    result = db.scalar(stmt)
    if result is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    db.add(user)
    db.commit()
    db.refresh(user)
    return vars(user)

@router.delete("/{user_id}")
def delete_users(current_user:UserModel = Depends(check_user_id), db = Depends(get_db)):
    stmt = delete(UserModel).where(UserModel.id == current_user.id)
    db.execute(stmt)
    db.commit()
    return {"message": "User deleted successfully"}

@router.patch("/update_optional/{user_id}", response_model=UserSchema.UserUpdateResponse)
def update_user_optional(user_update: UserSchema.UserBase, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    update_data = user_update.model_dump(exclude_unset=True)
    stmt = update(UserModel).where(UserModel.id == current_user.id).values(**update_data)
    db.execute(stmt)
    db.commit()
    stmt = select(UserModel).where(UserModel.id == current_user.id)
    result = db.scalar(stmt)
    return result
        
@router.put("/change_password/{user_id}")
def change_password(update_info: UserSchema.UserPasswordUpdate, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    if current_user.password != update_info.old_password:
        raise HTTPException(status_code=400, detail="Password validation failed")

    stmt = update(UserModel).where(UserModel.id == current_user.id).values(password=update_info.new_password)
    db.execute(stmt)
    db.commit()
    return {"message": "Password updated successfully"}
