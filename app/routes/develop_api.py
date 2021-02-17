from fastapi import APIRouter

from app.models import Base, engine

dev = APIRouter(prefix="/develop",
                tags=["develop"],
                responses={404: {"description": "Not found"}})


@dev.get('/drop')
def drop_create_db():
    Base.metadata.drop_all(bind=engine)
    return {"message": "Succesuful"}
