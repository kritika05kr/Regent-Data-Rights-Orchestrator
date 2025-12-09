# backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

# echo=True will print SQL queries in console (handy for debugging, but noisy)
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,  # SQLAlchemy 2.x style
)

# SessionLocal is a factory that creates new Session objects
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    FastAPI dependency.
    Yields a database session and makes sure it's closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
