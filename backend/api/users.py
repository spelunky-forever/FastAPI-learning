from fastapi import APIRouter, HTTPException, status
from schemas import users as UserSchema
from database.generic import get_db
from model.user import User as UserModel
from sqlalchemy import select, update, delete
from fastapi import Depends
from api.depends import check_user_id
from typing import Annotated
from api.depends import PaginationParams
from crud import users as UserCRUD
##from api.depends import test_vertify_token

CommonPaginationParams = Annotated[PaginationParams, Depends()]

##router = APIRouter(tags=["users"], prefix="/api/users", dependencies=[Depends(test_vertify_token)])
router = APIRouter(tags=["users"], prefix="/api/users")

@router.get("/",
         response_model= list[UserSchema.UserinforResponse],
)
async def get_users_infor(page_params: CommonPaginationParams, db = Depends(get_db)):
    return await UserCRUD.get_users_infor(keyword=page_params.keyword, last=page_params.last, limit=page_params.limit, db=db)

@router.get("/{user_id}", response_model= UserSchema.UserBase)
async def get_user_by_id(user_id: int, qry: str = None, db = Depends(get_db)):
    result = await UserCRUD.get_user_by_id(user_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/",
          response_model=UserSchema.UserRead,
          status_code=status.HTTP_201_CREATED
)
async def create_users(new_user: UserSchema.UserCreate, db = Depends(get_db)):
    result = await UserCRUD.create_users(new_user, db)
    if result is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return result

@router.delete("/{user_id}")
async def delete_users(current_user:UserModel = Depends(check_user_id), db = Depends(get_db)):
    result = await UserCRUD.delete_users(current_user, db)
    return result

@router.patch("/update_optional/{user_id}", response_model=UserSchema.UserUpdateResponse)
async def update_user_optional(user_update: UserSchema.UserBase, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    result = await UserCRUD.update_user_optional(user_update, db, current_user)
    return result
        
@router.put("/change_password/{user_id}")
async def change_password(update_info: UserSchema.UserPasswordUpdate, db = Depends(get_db), current_user:UserModel = Depends(check_user_id)):
    result = await UserCRUD.change_password(update_info, db, current_user)
    if result is None:
        raise HTTPException(status_code=400, detail="Password validation failed")
    return result
