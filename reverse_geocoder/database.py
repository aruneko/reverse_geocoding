from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = getenv("DB_USER", "geocoder")
DB_PASS = getenv("DB_PASS", "geocoder")
DB_HOST = getenv("DB_HOST", "localhost")
DB_NAME = getenv("DB_NAME", "geocoder")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
