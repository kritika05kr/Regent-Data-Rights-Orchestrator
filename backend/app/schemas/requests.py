from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


# ---------- Payload from frontend when creating a request ----------

class CreateRequestPayload(BaseModel):
    email: str
    customer_id: Optional[str] = None
    phone_last4: Optional[str] = None
    request_type: str
    message: Optional[str] = None


# ---------- Simple response for POST /requests ----------

class RequestCreateResponse(BaseModel):
    id: int
    status: str
    mode: str


# ---------- User-facing status view (GET /requests/{id}) ----------

class RequestStatusResponse(BaseModel):
    id: int
    request_type: str
    status: str
    mode: str
    email: str
    customer_id: Optional[str] = None
    phone_last4: Optional[str] = None
    message: Optional[str] = None
    user_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ---------- Admin list view (GET /admin/requests) ----------

class RequestAdminListItem(BaseModel):
    id: int
    email: str
    request_type: str
    status: str
    mode: str
    created_at: datetime
    updated_at: datetime


# ---------- Admin detail view (GET /admin/requests/{id}) ----------

class RequestAdminDetail(BaseModel):
    id: int
    email: str
    customer_id: Optional[str] = None
    phone_last4: Optional[str] = None
    request_type: str
    status: str
    mode: str
    message: Optional[str] = None
    user_summary: Optional[str] = None
    admin_report: Optional[str] = None
    logs: List[str] = []
    actions: List[Any] = []
    created_at: datetime
    updated_at: datetime
