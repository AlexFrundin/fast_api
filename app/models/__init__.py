from databases import Database

from .base import Base
from .user import User
from .pockemon import Pockemon, UserPockemon

from app.settings import DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_HOST

DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

database = Database(DATABASE_URI)
