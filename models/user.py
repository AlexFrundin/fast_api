from .base import Base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, String, Integer

from .pockemon import UserPockemon

metadata = Base.metadata

class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(20), unique=True)
    password_hash = Column(String(128))
    
    pockemons = association_proxy('pockemon_assoc', 'pockemon',
                                  creator=lambda pockemon: UserPockemon(pockemon=pockemon))
    
    def __str__(self) -> str:
        return f'{self.email}'
    
