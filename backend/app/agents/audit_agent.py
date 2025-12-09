from typing import Any


def run_audit_agent(state: Any) -> Any:
    """
    Builds a human-readable user summary and admin report from the state.
    """

    state.logs.append("AuditAgent: generating user summary and admin report.")

    # User-facing summary
    discovery_count = len(getattr(state, "discovery_results", []))
    actions_count = len(getattr(state, "deletion_actions", []))

    state.user_summary = (
        f"Your deletion request was processed in {state.mode} mode. "
        f"The system located {discovery_count} data locations and "
        f"simulated {actions_count} policy actions (mask/flag)."
    )

    # Admin-facing report
    lines = []
    lines.append(f"Request ID: {state.request_id}")
    lines.append(f"Email: {state.email}")
    lines.append(f"Customer ID: {state.customer_id or '-'}")
    lines.append(f"Phone last4: {state.phone_last4 or '-'}")
    lines.append(f"Mode: {state.mode}")
    lines.append(f"Final status: {state.status}")
    lines.append("")
    lines.append("Actions:")

    for action in getattr(state, "deletion_actions", []):
        lines.append(
            f"- [{action.get('status')}] {action.get('source_name')} "
            f"-> {action.get('action_type')} ({action.get('details')})"
        )

    state.admin_report = "\n".join(lines)

    state.logs.append("AuditAgent: summaries generated.")
    return state
