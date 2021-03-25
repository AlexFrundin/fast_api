from .base import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(20), unique=True)
    password_hash = Column(String(128))

    
    
