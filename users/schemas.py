from pydantic import BaseModel, EmailStr
from typing import Optional
from library.access.roles import Role


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.viewer


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[Role] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: Role

    class Config:
        from_attributes = True
