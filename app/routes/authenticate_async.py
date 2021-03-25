from fastapi import APIRouter, HTTPException, status

from app.schemas import UserCreate, UserToken
from app.crud_async import get_user_by_email, create_db_user, verify_password
from app.utils.utils import create_user_token

auth_async = APIRouter(prefix="/async/auth",
                 tags=["async-authenticate"],
                 responses={404: {"description": "Not found"}})


@auth_async.post('/register', response_model=UserToken, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate):
    if get_user_by_email(email=user.email):
        raise HTTPException(
            status_code=400, detail="Email already registered")
    _id = await create_db_user(user)
    return await create_user_token({'id': _id, **user.dict()})


@auth_async.post("/authenticate", response_model=UserToken, status_code=status.HTTP_200_OK)
async def authenticate_user(user: UserCreate):
    user = await get_user_by_email(email=user.email)
    if user is None:
        raise HTTPException(status_code=400, detail="User not existed")
    if not verify_password(user):
        raise HTTPException(status_code=400, detail="Password is not correct")
    return await create_user_token(user)
