from fastapi import APIRouter, HTTPException, status
from setting.config import get_settings
from database.fake_db import get_db

fake_db = get_db()

router = APIRouter(tags=["infor"],prefix="/api")

@router.get("/")
def hello_world():
    return "Hello World"

@router.get("/infor")
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

