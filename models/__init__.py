import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .user import User
from .pockemon import Pockemon, UserPockemon

DB_USER = os.environ.get("DB_USER") or 'test'
DB_PASS = os.environ.get("DB_PASS") or 'test123test'
DB_NAME = os.environ.get("DB_NAME") or 'test'
DB_HOST = os.environ.get("DB_HOST") or 'localhost'

DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
