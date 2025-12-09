from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from app.agents.identity_agent import run_identity_agent
from app.agents.discovery_agent import run_discovery_agent
from app.agents.policy_agent import run_policy_agent
from app.agents.audit_agent import run_audit_agent


@dataclass
class RegentState:
    """
    Single shared state object passed through all agents.
    """

    # Core identifiers
    request_id: int
    email: str
    customer_id: Optional[str] = None
    phone_last4: Optional[str] = None

    # Engine mode and status
    mode: str = "SIMULATION"
    status: str = "PENDING"

    # Flags
    identity_verified: bool = False

    # Pipeline artifacts
    logs: List[str] = field(default_factory=list)
    discovery_results: List[Dict[str, Any]] = field(default_factory=list)
    deletion_actions: List[Dict[str, Any]] = field(default_factory=list)

    # Final summaries
    user_summary: Optional[str] = None
    admin_report: Optional[str] = None


def run_regent_flow(state: RegentState) -> RegentState:
    """
    Orchestrates the full agentic pipeline in order:
    1) Identity
    2) Discovery
    3) Policy / actions
    4) Audit / summarisation
    """

    state.logs.append("Regent: starting pipeline.")

    state = run_identity_agent(state)
    state = run_discovery_agent(state)
    state = run_policy_agent(state)
    state = run_audit_agent(state)

    state.logs.append("Regent: pipeline completed.")
    return state
