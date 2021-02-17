from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import UserToken, UserCreate
from app.dependensies import get_db
from app.crud import get_user_by_email, create_db_user, verify_password
from app.utils import create_user_token 

auth = APIRouter(prefix="/user",
                 tags=["authenticate"],
                 responses={404: {"description": "Not found"}})


@auth.post("/create", response_model=UserToken, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=400, detail="Email already registered")
    return await create_user_token(create_db_user(db=db, user=user))


@auth.post("/authenticate", response_model=UserToken, status_code=status.HTTP_200_OK)
async def authenticate_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not existed")
    if not verify_password(db, user):
        raise HTTPException(status_code=400, detail="Password is not correct")
    return await create_user_token(db_user)
