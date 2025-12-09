# backend/app/db/models/user_profile.py

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime
from app.db.base import Base


class UserProfile(Base):
    """
    Stores basic user identity info.
    Used by IdentityAgent to verify that the requestor is who they claim to be.
    """

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # Identity fields
    email = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)  # full phone number
    dob = Column(Date, nullable=True)      # date of birth

    # Optional for realism
    full_name = Column(String, nullable=True)

    # Audit fields
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
