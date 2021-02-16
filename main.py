from typing import List

from fastapi import Depends, FastAPI, requests, status, HTTPException
from sqlalchemy.orm import Session

import uvicorn

import schemas
from crud import (check_username_password, create_db_user, get_user_by_email,
                  get_count_pockemons, create_pockemons, get_all_user,
                  create_pockemons_user)
from models import Base, engine, Pockemon, User
from depenses import get_db, get_params, get_current_user
from utils import get_pocki_api, create_user_token

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def update_or_create_data():
    answer = await get_pocki_api()
    db = next(get_db())
    if answer['count'] > get_count_pockemons(db):
        create_pockemons(db, answer['results'])


@app.post("/create", response_model=schemas.UserToken, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=400, detail="Email already registered")
    return await create_user_token(create_db_user(db=db, user=user))


@app.post("/authenticate", response_model=schemas.UserToken, status_code=status.HTTP_200_OK)
async def authenticate_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not existed")
    if not check_username_password(db, user):
        raise HTTPException(status_code=400, detail="Password is not correct")
    return await create_user_token(db_user)


@app.post("/add", status_code=status.HTTP_201_CREATED)
async def add_pockemon(pockemons: List[int],
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    create_pockemons_user(db, pockemons, user)
    return {"message": "Pockemons add"}


@app.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.UserCurrent])
async def get_users(user: schemas.UserCurrent = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    return get_all_user(db)


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user: schemas.UserCurrent = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return {"message": "User"}


@app.get('/my_profile', status_code=status.HTTP_200_OK, response_model=schemas.UserBase)
async def get_profile(user: User = Depends(get_current_user)):
    return user


@app.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.ListSchemaPockemonResponse)
async def get_all(user: schemas.UserCurrent = Depends(get_current_user),
                  params: schemas.Params = Depends(get_params),
                  db: Session = Depends(get_db)):
    """
    ?offset=%(offset)s&limit=%(limit)s
    """
    q = db.query(Pockemon)
    #add to redis_cash
    count = q.count()
    offset = params.offset
    limit = params.limit
    pockemons = db.query(Pockemon)[offset:limit]
    return {'count': count, 'offset': offset, 'limit':limit, 'pockemons':pockemons}


@app.get('/drop')
def drop_create_db():
    Base.metadata.drop_all(bind=engine)
    return {"message": "Succesuful"}



if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000,
                log_level="info", reload=True,
                debug=True, workers=2)
