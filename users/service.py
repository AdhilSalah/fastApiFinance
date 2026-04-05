from typing import List, Optional
from fastapi import HTTPException, status
from library.db.users import repository as repo
from library.db.users.models import User
from users.schemas import UserCreate, UserUpdate


def get_all_users(
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> List[User]:
    return repo.get_all(limit=limit, offset=offset, search=search, role=role, is_active=is_active)


def get_user(user_id: int) -> User:
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def create_user(data: UserCreate) -> User:
    if repo.get_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return repo.create(name=data.name, email=data.email, password=data.password)


def update_user(user_id: int, data: UserUpdate) -> User:
    user = repo.update(user_id, **data.model_dump(exclude_none=True))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def delete_user(user_id: int) -> None:
    if not repo.soft_delete(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
