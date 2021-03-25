from fastapi import APIRouter, Depends, status
from typing import List

from app.utils.dependensies import get_current_user_async, get_params, get_params_limit_offset
from app.schemas import (UserBase, SchemaPockemonResponse,
                         ParamsLimitOffset, CreateUserPockemon, SchemaPockemonBase)
from app import crud_async

user_async = APIRouter(prefix="/async/player",
                       tags=["async-player"],
                       dependencies=[Depends(get_current_user_async)],
                       responses={404: {"description": "Not found"}})


@user_async.get('/users', status_code=status.HTTP_200_OK, response_model=List[UserBase])
async def get_all():
    return await crud_async.get_all_users()


# @user_async.get('/profile/{id}', status_code=status.HTTP_200_OK, response_model=UserBase)
# async def get_user_profile(id: int):
#     data = await crud_async.get_user_by_id(id)
#     pockemons = [{'name': u.get('pname'), 'url': u.get('purl'), 'id': u.get('pid')}
#                  for u in data if u.get('pid')]
#     return {'email': data[0].get('email'), 'id': data[0].get('id'), 'pockemons': pockemons}


@user_async.get('/profile/{user_id}', status_code=status.HTTP_200_OK, response_model=List[SchemaPockemonBase])
async def get_user_profile(user_id: int):
    return await crud_async.get_user_pockemons(user_id)


@user_async.get('/pockemons/view', status_code=status.HTTP_200_OK, response_model=SchemaPockemonResponse)
async def get_count(params: ParamsLimitOffset = Depends(get_params_limit_offset)):
    pockemons = await crud_async.get_pockemons_offset(params)
    return {**params.dict(), 'pockemons': pockemons}


@user_async.post('/add', status_code=status.HTTP_201_CREATED)
async def add_user_pockemon(user: CreateUserPockemon):
    return await crud_async.create_pockemons_user(user)
    
    
