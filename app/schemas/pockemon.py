from typing import List
from datetime import datetime
from pydantic import BaseModel, HttpUrl, validator
from dateutil.tz import tzutc, tzlocal


class SchemaPockemon(BaseModel):
    name: str
    url: HttpUrl
  

class SchemaPockemonBase(SchemaPockemon):
    id: int
    createdAt: datetime
    
    @validator('createdAt')
    def processing_created_time(cls, v):
        utc_zone = tzutc()
        local_zone = tzlocal()
        _time = datetime.strptime(v)
        _time = _time.replace(tzinfo=utc_zone)
        local_time = _time.astimezone(local_zone)
        return local_time

class SchemaPockemonResponse(BaseModel):
    count: int
    limit: int = 20
    offset: int = 0
    pockemons: List[SchemaPockemonBase] 

    @validator('count')
    async def processing_count(cls, v):
        from app import crud_async
        return await crud_async.get_count_pockemons()
    
    class Config:
        allow_population_by_field_name = True

        

        
        
        
    
