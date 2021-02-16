from pydantic import BaseModel


class Params(BaseModel):
    limit: int = 1200
    offset: int = 0