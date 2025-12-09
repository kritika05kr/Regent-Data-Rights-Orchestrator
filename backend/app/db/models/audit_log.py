# backend/app/db/models/audit_log.py

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class AuditLog(Base):
    """
    Stores audit information for a request:
    - user-facing summary
    - admin-facing technical report
    - optional raw state snapshot (for debugging/demo)
    """

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Link back to the Request
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False, index=True)

    # Simple text summary shown to end user
    user_summary = Column(Text, nullable=True)

    # Detailed technical report for admins (tables, collections, files, actions)
    admin_report = Column(Text, nullable=True)

    # Optional: store raw JSON of agent State as string (for debugging)
    raw_state_json = Column(Text, nullable=True)

    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationship back to Request (useful in ORM)
    request = relationship("Request", backref="audit_logs")
