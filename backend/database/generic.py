from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from setting.config import get_settings

settings = get_settings()
url_object = settings.database_url
engine= create_engine(url_object)

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

def get_db():
    return SessionLocal()
