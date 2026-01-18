from fastapi import APIRouter, HTTPException, status
from setting.config import get_settings
from database.fake_db import get_db
from sqlalchemy import text
from database.generic import get_db

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

