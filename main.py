from app.settings import DEBUG
from fastapi import FastAPI

import uvicorn

from app.crud import get_count_pockemons, create_pockemons
from app.models import Base, engine
from app.dependensies import get_db
from app.utils import get_pocki_api

from app.routes import auth, user, pockemon, dev, video

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth)
app.include_router(user)
app.include_router(pockemon)
app.include_router(dev)
app.include_router(video)


@app.on_event("startup")
async def update_or_create_data():
    answer = await get_pocki_api()
    db = next(get_db())
    if answer['count'] > get_count_pockemons(db):
        create_pockemons(db, answer['results'])
  
      
@app.get('/')
async def root():
    return {"message": "Welcome to PockiLand Network API server :)"}


if __name__ == "__main__":
    if DEBUG:
        uvicorn.run('main:app', host="localhost", port=8000,
                    log_level="info", reload=True,
                    debug=True, workers=2)
    else:
        uvicorn.run('main:app', host="0.0.0.0", port=8000, workers=4)
