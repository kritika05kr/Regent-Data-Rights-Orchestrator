from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON

from app.db.base_class import Base


class DataRightsRequest(Base):
    """
    Core ORM model for GDPR / CCPA data-rights requests.
    This is what we store in the regent.db SQLite database.
    """

    __tablename__ = "data_rights_requests"

    id = Column(Integer, primary_key=True, index=True)

    # User identifiers
    email = Column(String, nullable=False, index=True)
    customer_id = Column(String, nullable=True, index=True)
    phone_last4 = Column(String(8), nullable=True)

    # Request metadata
    request_type = Column(String, nullable=False)  # e.g. "deletion"
    status = Column(String, nullable=False, default="PENDING", index=True)
    mode = Column(String, nullable=False, default="SIMULATION")  # SIMULATION / LIVE
    message = Column(Text, nullable=True)

    # Agentic pipeline outputs
    user_summary = Column(Text, nullable=True)
    admin_report = Column(Text, nullable=True)

    # Logs + actions stored as JSON arrays
    logs = Column(JSON, nullable=True)
    actions = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
