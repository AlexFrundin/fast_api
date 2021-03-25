from databases.backends.postgres import Record
from pydantic.networks import HttpUrl
from sqlalchemy import select, func, insert
from typing import List, Union, Iterable, Dict

from app.models import User, Pockemon, UserPockemon
from app.schemas import UserCurrent, UserCreate, ParamsLimitOffset, CreateUserPockemon
from app.models import database
from app.utils.utils import check_password, create_hash


async def verify_password(user: UserCurrent) -> bool:
    db_user = await get_user_by_email(email=user.email)
    return check_password(db_user.password_hash, user.password)


async def get_user_by_email(email: str) -> Union[Record, None]:
    stm = User.objects.select(User.email == email)
    return await database.fetch_one(stm)


async def get_all_users() -> List[Record]:
    return await database.fetch_all(User.objects.select())


async def get_user_by_id(id: int) -> Union[Record, None]:
    u, p, up = User.objects, Pockemon.objects, UserPockemon.objects
    stm = select([u, p.c.id.label('pid'), p.c.name.label('pname'), p.c.url.label('purl')])\
        .select_from(
        u.outerjoin(up, u.c.id == up.c.user_id).
        outerjoin(p, p.c.id == up.c.pockemon_id)
    ).where(u.c.id == id)

    return await database.fetch_all(stm)


async def get_count_pockemons() -> int:
    return await database.fetch_one(select([func.count().label("count")]).select_from(Pockemon))


async def create_pockemons(pockemons: List[Dict[str, Union[str, HttpUrl]]]) -> List[int]:
    return await database.execute_many(Pockemon.objects.insert().values(**pockemons))


async def create_db_user(user: UserCreate) -> int:
    password_hash = create_hash(user.password)
    stm = insert(User)
    values = {'email': user.email, 'password_hash': password_hash}
    # stm = User.objects.insert()
    return await database.execute(stm, values)


async def get_pockemons_list(ids: List[int]) -> Iterable[Record]:
    stm = Pockemon.objects.select(Pockemon.id.in_(ids))
    return await database.fetch_all(stm)


async def create_pockemons_user(user: CreateUserPockemon):
    stm = insert(UserPockemon)
    values = [{'user_id': user.id, 'pockemon_id': _id} for _id in user.pockemons]
    return await database.execute_many(stm, values)


async def get_pockemons_offset(params: ParamsLimitOffset) -> Iterable[Record]:
    stm = select([Pockemon]).offset(params.offset).limit(params.limit)
    return await database.fetch_all(stm)


async def get_user_pockemons(user_id: int) -> Iterable[Record]:
    u, p, up = User.objects, Pockemon.objects, UserPockemon.objects
    stm = select([p]).select_from(
        up.outerjoin(u, u.c.id == up.c.user_id).
        outerjoin(p, p.c.id == up.c.pockemon_id)
    ).where(u.c.id == user_id)
    return await database.fetch_all(stm)
