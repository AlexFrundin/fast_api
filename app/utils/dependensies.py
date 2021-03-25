from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt

from app import schemas
from app.utils.utils import decode_access_token
from app import crud_async

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")



async def get_params(request: Request):
    return request.query_params

async def get_params_limit_offset(request: Request):
    return schemas.ParamsLimitOffset(**request.query_params)


async def get_params_id(request: Request):
    return schemas.ParamsIdUser(**request.query_params)


async def get_current_user_async(user: schemas.UserCurrent, token: str = Depends(oauth2_scheme)):
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
        if (user := await crud_async.get_user_by_email(email=user.email)):
            return user
    raise HTTPException(**_exception)
