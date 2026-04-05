from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from library.auth.schemas import Token
from library.auth import service
from library.auth.dependencies import get_current_user
from library.db.users.models import User
from users.schemas import UserResponse

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 login — use email in the 'username' field."""
    user = service.authenticate_user(email=form.username, password=form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = service.create_access_token(data={"sub": user.email})
    return Token(access_token=token, token_type="bearer")


@router.post("/logout")
async def logout():
    # Stateless JWT — client must discard the token
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    """Returns the currently authenticated user."""
    return current_user
