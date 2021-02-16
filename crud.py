from sqlalchemy.orm import Session
from typing import Union, List

from app.utils import check_password, create_hash
from app.models import User, Pockemon
import schemas


def get_user_by_id(db: Session, id:int) -> Union[User, None]:
    return db.query(User).get(id == 1)


def get_count_pockemons(db: Session):
    return db.query(Pockemon).count()


def create_pockemons(db: Session, pockemons: List[dict]):
    to_pockemons = [Pockemon(**item) for item in pockemons]
    db.add_all(to_pockemons)
    db.commit()
    return True


def get_user_by_email(db: Session, email: str) -> Union[User, None]: 
    return db.query(User).filter(User.email == email).first()
     

def check_username_password(db: Session, user: schemas.UserCreate) -> bool:
    db_user = get_user_by_email(db, email=user.email)
    return check_password(db_user.password_hash, user.password)


def create_db_user(db: Session, user: schemas.UserCreate) -> User:
    password_hash = create_hash(user.password)
    db_user = User(email=user.email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    return db_user


def get_all_user(db: Session) -> List[User]:
    return db.query(User).all()


def get_pockemons_list(db: Session, ids: List[int]) -> List[Pockemon]:
    return db.query(Pockemon).filter(Pockemon.id.in_(ids)).all()


def create_pockemons_user(db: Session, ids: List[int], user: User)->bool:
    user.pockemons.extend(get_pockemons_list(db, ids))
    db.commit()
    return True 
