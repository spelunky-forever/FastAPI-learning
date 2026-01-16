from fastapi import FastAPI, HTTPException, status
from setting.config import get_settings
from schemas import users as UserSchema
from schemas import items as ItemSchema
from database.fake_db import get_db

fake_db = get_db()

app = FastAPI()

@app.get("/")
def hello_world():
    return "Hello World"

@app.get("/users",
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

@app.get("/users/{user_id}", response_model= UserSchema.UserRead)
def get_user_by_id(user_id: int, qry: str = None):
    for user in fake_db["users"]:
        if user["id"]==user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users",
          response_model=UserSchema.UserRead,
          status_code=status.HTTP_201_CREATED
)
def create_users(user: UserSchema.UserCreate):
    fake_db["users"].append(user)
    return user

@app.post("/userCreate" , deprecated=True)
def create_user_deprecated(newUser: UserSchema.UserCreate ):
    return "deprecated"

@app.delete("/users/{user_id}" )
def delete_users(user_id: int):
    for user in fake_db["users"]:
        if user["id"]==user_id:
            fake_db["users"].remove(user)
            return user
    return {"error": "User not found"}


@app.get("/items/{item_id}", response_model= ItemSchema.ItemRead)
def get_item_by_id(item_id: int, qry: str= None):
    if item_id not in fake_db["items"]:
        return {"error": "Item not found"}
    return fake_db['items'][item_id]

@app.post("/items", response_model= ItemSchema.ItemCreate)
def create_items(item: ItemSchema.ItemCreate):
    fake_db["items"][item.id] = item
    return item

@app.delete("/items/{item_id}")
def delete_items(item_id: int):
    item = fake_db["items"].pop(item_id)
    return item

@app.get("/infor")
def get_infor():
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "app_mode": settings.app_mode,
        "port": settings.port,
        "reload": settings.reload,
        "database_url": settings.database_url
    }