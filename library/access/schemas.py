from pydantic import BaseModel
from typing import List
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class Permission(BaseModel):
    user_id: int
    role: Role
    resource: str


class PermissionCreate(BaseModel):
    user_id: int
    role: Role
    resource: str


class PermissionResponse(BaseModel):
    id: int
    user_id: int
    role: Role
    resource: str

    class Config:
        from_attributes = True
