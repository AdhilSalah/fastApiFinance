from typing import List, Optional
import bcrypt
from datetime import datetime
from sqlalchemy import func
from library.db.database import db_session
from library.db.users.models import User


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def get_all(
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> List[User]:
    with db_session() as db:
        query = db.query(User).filter(User.deleted_at == None)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (User.name.ilike(search_filter)) | (User.email.ilike(search_filter))
            )
            
        if role:
            query = query.filter(User.role == role)
            
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
            
        return query.offset(offset).limit(limit).all()


def get_by_id(user_id: int) -> Optional[User]:
    with db_session() as db:
        return db.query(User).filter(User.id == user_id,User.deleted_at == None).first()


def get_by_email(email: str) -> Optional[User]:
    with db_session() as db:
        return db.query(User).filter(User.email == email,User.deleted_at == None).first()


def create(name: str, email: str, password: str) -> User:
    with db_session() as db:
        user = User(name=name, email=email, hashed_password=_hash(password))
        db.add(user)
        db.flush()
        db.refresh(user)
        return user


def update(user_id: int, **kwargs) -> Optional[User]:
    with db_session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        if "password" in kwargs:
            kwargs["hashed_password"] = _hash(kwargs.pop("password"))
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        db.flush()
        db.refresh(user)
        return user


def delete(user_id: int) -> bool:
    with db_session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        return True
def soft_delete(user_id: int) -> bool:
    with db_session() as db:
        user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
        if not user:
            return False
        user.deleted_at = func.now()
        return True
