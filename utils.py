import jwt
from datetime import timedelta, datetime
import bcrypt
import httpx

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_MINUTES_TEST = 300000

all_pockemon = "https://pokeapi.co/api/v2/pokemon/?offset=%(offset)s&limit=%(limit)s"


def create_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))


async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    delta_time =  expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + delta_time
    to_encode = {"exp": expire, **data}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(*, token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def create_user_token(db_user, expires_dalta: int = ACCESS_TOKEN_EXPIRE_MINUTES_TEST):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES_TEST)
    access_token = await create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, **db_user.__dict__}


async def get_pocki_api():
    async with httpx.AsyncClient() as client:
        data = await client.get(all_pockemon % {"offset": 0, "limit": 1200})
        return data.json()
