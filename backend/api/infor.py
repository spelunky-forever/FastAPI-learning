from fastapi import APIRouter, HTTPException, status
from setting.config import get_settings
from database.fake_db import get_db
from sqlalchemy import text
from database.generic import get_db
from model.user import User
from model.item import Item

fake_db = get_db()

router = APIRouter(tags=["infor"],prefix="/api")

@router.get("/")
def hello_world():
    return "Hello World"

@router.get("/infor")
def get_infor():
    database=None
    db_session = get_db()
    try:
        database = db_session.execute(text("SELECT datname FROM pg_database;")).fetchall()
    except Exception as e:
        print(e)
    
    if database is None:
        try:
            database = db_session.execute(text("SHOW DATABASES;")).fetchall()
        except Exception as e:
            print(e)

    settings = get_settings()

    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "app_mode": settings.app_mode,
        "port": settings.port,
        "reload": settings.reload,
        "db_type": settings.db_type,
        "database_url": settings.database_url,
        "database": str(database)
    }

@router.get("/test/insert")
def test():
    db_session = get_db()
    result = {"user": None, "items": None, "user.items": None}
    try:
        test_user = User("123456", "test0", 0, None, "2000-01-01", "123@email.com")
        db_session.add(test_user)
        db_session.commit()
        result["user"] = test_user

        test_item = Item("item0",99.9, "brand0", "test0", test_user.id)
        db_session.add(test_item)
        db_session.commit()
        result["item"] = test_item

        result["user.items"] = test_user.items
    except Exception as e:
        print(e)

    return result
    


