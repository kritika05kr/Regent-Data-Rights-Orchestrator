from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.request import DataRightsRequest
from app.schemas.requests import (
    CreateRequestPayload,
    RequestCreateResponse,
    RequestStatusResponse,
)
from app.services.request_service import create_and_start_request

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestCreateResponse)
def create_request(
    payload: CreateRequestPayload,
    db: Session = Depends(get_db),
) -> RequestCreateResponse:
    """
    Create a new data-rights request and run the Regent agentic flow.
    Returns just: id, status, mode.
    """
    req = create_and_start_request(payload, db)
    return RequestCreateResponse(
        id=req.id,
        status=req.status,
        mode=req.mode,
    )


@router.get("/{request_id}", response_model=RequestStatusResponse)
def get_request_status(
    request_id: int,
    db: Session = Depends(get_db),
) -> RequestStatusResponse:
    """
    User-facing status endpoint for a single request.
    """
    req = db.query(DataRightsRequest).get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    return RequestStatusResponse(
        id=req.id,
        request_type=req.request_type,
        status=req.status,
        mode=req.mode,
        email=req.email,
        customer_id=req.customer_id,
        phone_last4=req.phone_last4,
        message=req.message,
        user_summary=req.user_summary,
        created_at=req.created_at,
        updated_at=req.updated_at,
    )
