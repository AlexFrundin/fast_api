from pydantic import BaseModel, validator
from typing import List, Optional
from app.schemas import SchemaPockemonBase


class Token(BaseModel):
    access_token: str
    type_token: str = "Bearer"


class User(BaseModel):
    email: str


class UserCreate(User):
    password: str


class UserCurrent(User):
    id: int
    

class UserBase(UserCurrent):
    pockemons: Optional[List[SchemaPockemonBase]]
    
    @validator('pockemons', pre=True)
    def evalute_pockemons(cls, v):
        return list(v)

class UserToken(Token, UserCurrent):
    pass


class CreateUserPockemon(UserCurrent):
    pockemons: List[int]
