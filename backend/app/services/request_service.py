from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.request import DataRightsRequest
from app.schemas.requests import CreateRequestPayload
from app.agents.graph import RegentState, run_regent_flow

settings = get_settings()


def create_and_start_request(payload: CreateRequestPayload, db: Session) -> DataRightsRequest:
    """
    1) Create DB row with initial PENDING status
    2) Build RegentState
    3) Run full agentic pipeline
    4) Update DB row with final status + summaries
    """

    # 1) Insert initial row
    obj = DataRightsRequest(
        email=payload.email,
        customer_id=payload.customer_id,
        phone_last4=payload.phone_last4,
        request_type=payload.request_type,
        status="PENDING",
        mode=settings.MODE,
        message=payload.message,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # 2) Build initial state for the agent pipeline
    state = RegentState(
        request_id=obj.id,
        email=obj.email,
        customer_id=obj.customer_id,
        phone_last4=obj.phone_last4,
        mode=obj.mode,
        status=obj.status,
    )

    # 3) Run pipeline
    final_state = run_regent_flow(state)

    # 4) Update DB row with final outputs
    obj.status = final_state.status
    obj.user_summary = final_state.user_summary
    obj.admin_report = final_state.admin_report
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj
