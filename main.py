from typing import List
from app.schemas import  CreateUserPockemon
from fastapi import FastAPI, status
from starlette.status import HTTP_200_OK

import uvicorn

from app.settings import DEBUG, ENV, APP_PORT, APP_HOST
from app.models import database
from app.routes import video, auth_async, user_async

app = FastAPI()

app.include_router(video)
app.include_router(auth_async)
app.include_router(user_async)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def start_app():
    if ENV == 'develompent' :
        uvicorn.run('main:app', host=APP_HOST, port=APP_PORT,
                    log_level="info", reload=DEBUG,
                    debug=DEBUG, workers=2)
    else:
        uvicorn.run('main:app', host=APP_HOST, port=APP_PORT, workers=4)


@app.get('/', status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to PockiLand Network API server :)"}

from app import crud_async
@app.get('/test/{id}')
async def get_p(id: int):
    p = await crud_async.get_user_pockemons(id)
    ids = [(dict(i)) for i in p]
    return {'ids': ids}


@app.post('/add', status_code=status.HTTP_201_CREATED)
async def add_user_pockemon(user: CreateUserPockemon):
    await crud_async.create_pockemons_user(user)
    return {"message": "Ok"}

@app.get('/get/{email}')
async def get_user(email: str):
    user = await crud_async.get_user_by_email(email)
    pocki = await crud_async.get_pockemons_list([1,2,3])
    
    return pocki

if __name__ == "__main__":
    start_app()
