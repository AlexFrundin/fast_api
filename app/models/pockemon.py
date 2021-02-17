from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, String, Integer

from .base import Base

metadata = Base.metadata


class Pockemon(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    url = Column(String(50))
    
    def __str__(self):
        return f'{self.id} with {self.name}'
    
    def __repr__(self):
        return self.__str__()
   

class UserPockemon(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    pockemon_id = Column(ForeignKey('pockemon.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship('User', backref=backref(
        'pockemon_assoc', passive_deletes=True,
        cascade='all, delete-orphan'))
    pockemon = relationship('Pockemon', backref=backref(
        'user_assoc', passive_deletes=True,
        cascade='all, delete-orphan'))
