from typing import Any


def run_identity_agent(state: Any) -> Any:
    """
    Simple demo identity verification.

    Logic:
    - If email looks valid (contains '@')
    - AND at least one of (customer_id, phone_last4) is present
      → identity_verified = True
      → status = 'IDENTITY_VERIFIED'
    - Otherwise → identity_verified = False, status = 'REJECTED'
    """

    state.logs.append("IdentityAgent: starting identity verification.")

    email_ok = bool(state.email and "@" in state.email)
    extra_id_ok = bool(state.customer_id or state.phone_last4)

    if email_ok and extra_id_ok:
        state.identity_verified = True
        state.status = "IDENTITY_VERIFIED"
        state.logs.append(
            "IdentityAgent: identity verified using demo rules (email + one extra identifier)."
        )
    else:
        state.identity_verified = False
        state.status = "REJECTED"
        state.logs.append(
            "IdentityAgent: identity verification failed (missing/invalid identifiers)."
        )

    return state
