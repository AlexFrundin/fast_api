from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field
from pydantic.class_validators import validator, root_validator

class SchemaPockemon(BaseModel):
    id: int
    name: str
  

class SchemaPockemonBase(SchemaPockemon):
    class Config:
        orm_mode = True
  
        
class SchemaPockemonResponse(SchemaPockemon):   

    url: HttpUrl
    
    @root_validator(pre=True)
    def get_id_to_url(cls, values):
        id = values.get('url').split('/')[-2]
        values.update({'id': id})
        return values        
    

class ListSchemaPockemonResponse(BaseModel):
    count: int
    limit: Optional[HttpUrl]
    page_offset: Optional[HttpUrl]
    pockemons: List[SchemaPockemonResponse] = Field(..., alias="results")
    
    class Config:
        allow_population_by_field_name = True
    

    @validator('next', 'previous')
    def processing_url(cls, v):
        # https://pokeapi.co/api/v2/pokemon/?offset=20&limit=20
        MY_URL_GET_POCKEMONS = 'http://127.0.0.1:8000/pockemons/'
        if v:
            _, params = v.split('?')
            return "?".join((MY_URL_GET_POCKEMONS, params))
        
        
        
    
