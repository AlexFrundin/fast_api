from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from datetime import datetime

from .base import Base

class Pockemon(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    url = Column(String(50))
   

class UserPockemon(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    pockemon_id = Column(ForeignKey('pockemon.id', ondelete='CASCADE'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
