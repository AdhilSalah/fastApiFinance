from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from library.auth import service
from library.db.users import repository as user_repo
from library.db.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """FastAPI dependency — validates JWT and returns the logged-in User."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = service.decode_token(token)
    if not token_data or not token_data.email:
        raise credentials_exception

    user = user_repo.get_by_email(token_data.email)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user
