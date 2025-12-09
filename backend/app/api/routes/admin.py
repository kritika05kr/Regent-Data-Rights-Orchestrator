from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.request import DataRightsRequest
from app.schemas.requests import (
    RequestAdminListItem,
    RequestAdminDetail,
)

router = APIRouter(prefix="/admin/requests", tags=["admin"])


@router.get("", response_model=List[RequestAdminListItem])
def list_requests(db: Session = Depends(get_db)) -> List[RequestAdminListItem]:
    objs = (
        db.query(DataRightsRequest)
        .order_by(DataRightsRequest.created_at.desc())
        .all()
    )
    return [
        RequestAdminListItem(
            id=o.id,
            email=o.email,
            request_type=o.request_type,
            status=o.status,
            mode=o.mode,
            created_at=o.created_at,
            updated_at=o.updated_at,
        )
        for o in objs
    ]


@router.get("/{request_id}", response_model=RequestAdminDetail)
def get_request_detail(
    request_id: int, db: Session = Depends(get_db)
) -> RequestAdminDetail:
    o = db.query(DataRightsRequest).get(request_id)
    if not o:
        raise HTTPException(status_code=404, detail="Request not found")

    return RequestAdminDetail(
        id=o.id,
        email=o.email,
        customer_id=o.customer_id,
        phone_last4=o.phone_last4,
        request_type=o.request_type,
        status=o.status,
        mode=o.mode,
        message=o.message,
        user_summary=o.user_summary,
        admin_report=o.admin_report,
        logs=o.logs or [],
        actions=o.actions or [],
        created_at=o.created_at,
        updated_at=o.updated_at,
    )
