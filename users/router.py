from fastapi import Depends
from typing import List, Optional
from library.access.router import AccessRouter, Access
from library.access.permissions import Resource, Action
from library.auth.dependencies import get_current_user
from library.db.users.models import User
from users.schemas import UserCreate, UserUpdate, UserResponse
import users.service as service

router = AccessRouter()


# Public — anyone can register
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate):
    return service.create_user(data)


# Protected — require valid JWT and Read permission
@router.get("/", response_model=List[UserResponse])
@Access(Resource.User, Action.Read)
async def list_users(
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    return service.get_all_users(limit=limit, offset=offset, search=search, role=role, is_active=is_active)


@router.get("/{user_id}", response_model=UserResponse)
@Access(Resource.User, Action.Read)
async def get_user(user_id: int):
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
@Access(Resource.User, Action.Update)
async def update_user(user_id: int, data: UserUpdate):
    return service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=204)
@Access(Resource.User, Action.Delete)
async def delete_user(user_id: int):
    service.delete_user(user_id)
