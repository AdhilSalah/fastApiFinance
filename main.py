from fastapi import FastAPI, Depends
from library.db.database import engine, Base

# Import all models so SQLAlchemy creates their tables
import library.db.users.models  # noqa: F401
import library.db.finance.models  # noqa: F401

from users.router import router as users_router
from finance.router import router as finance_router
from library.auth.router import router as auth_router
from library.auth.dependencies import get_current_user
from library.seeder import seed_admin

# Create all tables on startup, then seed default data
Base.metadata.create_all(bind=engine)
seed_admin()

app = FastAPI(
    title="Finance FastAPI App",
    description="A FastAPI application with users, finance, and library modules",
    version="1.0.0",
)

# Include routers
# auth  → public  (login must be reachable without a token)
# users → public router handles its own per-route auth (POST /users/ is open for registration)
# finance & access → fully protected at router level
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"],dependencies=[Depends(get_current_user)])
app.include_router(finance_router, prefix="/finance", dependencies=[Depends(get_current_user)], tags=["Finance"])


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Finance FastAPI App"}
