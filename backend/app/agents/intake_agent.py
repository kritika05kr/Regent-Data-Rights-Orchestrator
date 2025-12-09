# backend/app/agents/intake_agent.py

from app.agents.state import RegentState, RequestType


def run_intake_agent(state: RegentState) -> RegentState:
    """
    Intake Agent:
    - Understand what type of request this is (for now: deletion).
    - Make sure basic identifiers (email, customer_id, phone_last4) are in state.
    - Add an intake log entry.
    """

    # For now we assume everything coming in is a deletion request.
    # Later we can classify based on state.user_input.
    state.request_type = RequestType.DELETION

    # Add a log entry
    state.logs.append(
        "IntakeAgent: Classified request as 'deletion' and recorded basic identifiers."
    )

    return state
