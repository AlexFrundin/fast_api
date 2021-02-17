from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field
from pydantic.class_validators import validator, root_validator


class SchemaPockemon(BaseModel):
    name: str
    url: HttpUrl
  

class SchemaPockemonBase(SchemaPockemon):
    id: int
    
    class Config:
        orm_mode = True



class ListSchemaPockemonResponse(BaseModel):
    count: int 
    limit: int = 20
    offset: int = 0
    pockemons: List[SchemaPockemonBase] = Field(..., alias="results")
    
    class Config:
        allow_population_by_field_name = True
        
        

        
        
        
    
