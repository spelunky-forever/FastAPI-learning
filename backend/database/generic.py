from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from setting.config import get_settings
from model.user import User
from model.item import Item

settings = get_settings()
url_object = settings.database_url
engine= create_engine(url_object,echo=True)

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine, tables=[User.__table__, Item.__table__])
