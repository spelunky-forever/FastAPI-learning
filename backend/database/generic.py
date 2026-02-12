from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from setting.config import get_settings
from model.user import User
from model.item import Item

settings = get_settings()
url_object = settings.database_url
engine= create_async_engine(url_object,echo=True)

SessionLocal= async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base= declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[User.__table__, Item.__table__])