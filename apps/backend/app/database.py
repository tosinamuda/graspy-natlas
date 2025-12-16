from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.settings import get_settings

settings = get_settings()

# SQLite database URL
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create engine
# check_same_thread=False is needed for SQLite in multithreaded (FastAPI) envs
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get DB session.
    Yields session and closes it after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
