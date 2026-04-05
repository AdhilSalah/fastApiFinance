from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# expire_on_commit=False keeps ORM objects readable after the session closes
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


@contextmanager
def db_session():
    """Context manager that opens a session, commits on success, rolls back on error."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
