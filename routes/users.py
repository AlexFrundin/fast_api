from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.dependensies import get_current_user, get_db, get_params_id
from app.crud import create_pockemons_user, get_all_user, get_user_by_id
from app.models import User
from app.schemas import UserCurrent, UserBase, ParamsIdUser
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND


user = APIRouter(prefix="/player",
                 tags=["player"],
                 dependencies=[Depends(get_current_user)],
                 responses={404: {"description": "Not found"}})


@user.post("/add-pockemons", status_code=status.HTTP_201_CREATED)
async def add_pockemon(pockemons: List[int],
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    create_pockemons_user(db, pockemons, user)
    return {"message": "Pockemons add"}


@user.get("/all", status_code=status.HTTP_200_OK, response_model=List[UserCurrent])
async def get_users(db: Session = Depends(get_db)):
    return get_all_user(db)


@user.get("/get", status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_user( user_id: ParamsIdUser = Depends(get_params_id),
                    user: UserCurrent = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    print(user_id)
    print(user_id.id)
    if not (_user := get_user_by_id(db, user_id.id)) is None:
        return _user
    return Response(status.HTTP_404_NOT_FOUND)


@user.get('/profile', status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_profile(user: User = Depends(get_current_user)):
    return user
