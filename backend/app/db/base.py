# backend/app/db/base.py

from sqlalchemy.orm import declarative_base

# All our models will inherit from this Base
Base = declarative_base()
