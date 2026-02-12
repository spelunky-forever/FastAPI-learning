from fastapi import APIRouter, HTTPException, status, Depends
from setting.config import get_settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database.generic import get_db
from model.user import User
from model.item import Item

router = APIRouter(tags=["infor"], prefix="/api")

@router.get("/")
async def hello_world():
    return "Hello World"

@router.get("/infor")
async def get_infor(db: AsyncSession = Depends(get_db)):
    database = None

    try:
        # execute 回傳的是 Result 物件，要 await 執行，再 fetchall
        result = await db.execute(text("SELECT datname FROM pg_database;"))
        database = result.fetchall()
    except Exception as e:
        print(f"Postgres check failed: {e}")
    
    if database is None:
        try:
            result = await db.execute(text("SHOW DATABASES;"))
            database = result.fetchall()
        except Exception as e:
            print(f"MySQL check failed: {e}")

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
async def test(db: AsyncSession = Depends(get_db)):
    result = {"user": None, "items": None, "user.items": None}
    try:
        test_user = User("123456", "test0", 0, None, "2000-01-01", "123@email.com")
        db.add(test_user)
        await db.commit()        
        await db.refresh(test_user) 
        result["user"] = test_user

        test_item = Item("item0", 99.9, "brand0", "test0", test_user.id)
        db.add(test_item)
        await db.commit()       
        await db.refresh(test_item) 
        result["item"] = test_item

        # 【重要坑點】讀取關聯 (Relationship)
        # 在 Async 模式下，直接讀取 test_user.items 會報錯 (MissingGreenlet)，因為它預設是同步懶加載。
        # 最簡單的解法是再次 refresh 並明確指定要載入的屬性
        await db.refresh(test_user, attribute_names=["items"]) 
        result["user.items"] = test_user.items
        
    except Exception as e:
        print(f"Insert test failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return result