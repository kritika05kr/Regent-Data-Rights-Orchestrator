# backend/app/db/models/customer_order.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class CustomerOrder(Base):
    """
    Example table that contains user-related data (PII).
    We will use this for Discovery + Deletion simulation.
    """

    __tablename__ = "customer_orders"

    id = Column(Integer, primary_key=True, index=True)

    # Link fields
    user_email = Column(String, index=True, nullable=False)
    customer_id = Column(String, index=True, nullable=True)

    # Example PII fields
    order_number = Column(String, nullable=False)
    shipping_address = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
