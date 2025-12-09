# backend/app/api/deps.py

from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import get_db as _get_db


def get_db() -> Generator[Session, None, None]:
    """
    Wrapper around the SessionLocal dependency.
    We define it here so routers can import from api.deps.
    """
    yield from _get_db()
