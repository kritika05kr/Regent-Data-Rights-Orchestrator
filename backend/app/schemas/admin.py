# backend/app/schemas/admin.py

from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class AdminRequestListItem(BaseModel):
    id: int
    request_type: str
    status: str
    user_email: str
    user_customer_id: Optional[str]
    mode: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


class DeletionActionView(BaseModel):
    """
    Simple representation of an action for admin view.
    """

    source_name: str
    location_type: str
    action_type: str
    status: str
    details: Optional[str] = None


class AdminRequestDetail(BaseModel):
    id: int
    request_type: str
    status: str
    user_email: str
    user_customer_id: Optional[str]
    mode: str
    created_at: datetime
    updated_at: datetime

    user_summary: Optional[str]
    admin_report: Optional[str]

    deletion_actions: List[DeletionActionView] = []

    class Config:
        from_attributes = True
