from fastapi import APIRouter, HTTPException, status
from schemas import users as UserSchema
from database.fake_db import get_db

fake_db = get_db()

router = APIRouter(tags=["users"],prefix="/api/users")

@router.get("/",
         response_model= list[UserSchema.UserRead],
         #description="Get list of users"
)
def get_users_list(qry: str = None):
    """
    Create an user list with all the information:

    - **id**
    - **name**
    - **email**
    - **avatar**

    """
    return fake_db["users"]

@router.get("/{user_id}", response_model= UserSchema.UserRead)
def get_user_by_id(user_id: int, qry: str = None):
    for user in fake_db["users"]:
        if user["id"]==user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/",
          response_model=UserSchema.UserRead,
          status_code=status.HTTP_201_CREATED
)
def create_users(user: UserSchema.UserCreate):
    fake_db["users"].append(user)
    return user

@router.delete("/{user_id}")
def delete_users(user_id: int):
    for user in fake_db["users"]:
        if user["id"]==user_id:
            fake_db["users"].remove(user)
            return user
    return {"error": "User not found"}

