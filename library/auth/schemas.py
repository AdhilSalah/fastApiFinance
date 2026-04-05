from pydantic import BaseModel, EmailStr
from typing import Optional


class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
