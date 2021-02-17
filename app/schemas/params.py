from pydantic import BaseModel


class ParamsLimitOffset(BaseModel):
    limit: int = 1200
    offset: int = 0
    

class ParamsIdUser(BaseModel):
    id: int