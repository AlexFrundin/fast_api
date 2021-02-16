from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import jwt
import httpx
from starlette.status import HTTP_401_UNAUTHORIZED

from models import SessionLocal
from schemas import Params, UserCurrent
from utils import create_user_token, decode_access_token
from crud import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_params(request: Request):
    return Params(**request.query_params)


async def get_current_user(user: UserCurrent, token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)):
    _exception = {'status_code': status.HTTP_401_UNAUTHORIZED,
                  'detail': "Could not validate credentials",
                  'headers': {"WWW-Authenticate": "Bearer"}}
    try:
        payload = decode_access_token(token=token)
    except jwt.ExpiredSignatureError:
        _exception['detail'] = "Signature has expired"
        raise HTTPException(**_exception)
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        raise HTTPException(**_exception)
    if user.email == payload.get("sub"):
        if (user := get_user_by_email(db, email=user.email)):
            return user
    raise HTTPException(**_exception)
