# backend/app/db/models/request.py

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.base import Base


class Request(Base):
    """
    Represents a single data subject request (e.g., deletion under GDPR/CCPA).
    """

    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    # For now, main type = "deletion", but later we can add "access", "rectification", etc.
    request_type = Column(String, nullable=False, default="deletion")

    # Status as simple string:
    # "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"
    status = Column(String, nullable=False, default="PENDING")

    # Basic user identifiers (for quick filtering in admin UI)
    user_email = Column(String, index=True, nullable=False)
    user_customer_id = Column(String, index=True, nullable=True)

    # Raw message / reason / free text from user
    message = Column(Text, nullable=True)

    # Optional: store the "mode" (SIMULATION or LIVE) used for this request
    mode = Column(String, nullable=False, default="SIMULATION")

    # Timestamps
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
