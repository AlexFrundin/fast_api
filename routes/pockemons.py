from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas import ListSchemaPockemonResponse, ParamsLimitOffset
from app.models import Pockemon
from app.dependensies import get_db, get_current_user, get_params_limit_offset

pockemon = APIRouter(prefix="/pockemons",
                     tags=["pockemons"],
                     dependencies=[Depends(get_current_user)],
                     responses={404: {"description": "Not found"}})


@pockemon.get('/view', status_code=status.HTTP_200_OK, response_model=ListSchemaPockemonResponse)
async def get_pockemons(ParamsLimitOffset: ParamsLimitOffset = Depends(get_params_limit_offset),
                  db: Session = Depends(get_db)):
    """
    get array pockemons
    ?offset=%(offset)s&limit=%(limit)s
    """
    q = db.query(Pockemon)
    #add to redis_cash
    count = q.count()
    offset = ParamsLimitOffset.offset
    limit = ParamsLimitOffset.limit
    pockemons = db.query(Pockemon)[offset:limit]
    return {'count': count, 'offset': offset, 'limit': limit, 'pockemons': pockemons}
