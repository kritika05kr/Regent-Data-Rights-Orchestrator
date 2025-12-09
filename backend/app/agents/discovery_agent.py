from typing import Any, Dict, List


def run_discovery_agent(state: Any) -> Any:
    """
    Simulated data discovery.

    If identity is not verified, we skip discovery.
    Otherwise, we pretend to find PII in a couple of SQL sources.
    """

    state.logs.append("DiscoveryAgent: starting discovery step.")

    if not getattr(state, "identity_verified", False):
        state.logs.append(
            "DiscoveryAgent: identity not verified, skipping data discovery."
        )
        return state

    results: List[Dict] = []

    if state.email:
        # Simulate that we found this email in a customer and orders table
        results.append(
            {
                "source": "sql:customers",
                "location_type": "row",
                "pii_type": "email",
                "identifier": state.email,
            }
        )
        results.append(
            {
                "source": "sql:orders",
                "location_type": "row",
                "pii_type": "email",
                "identifier": state.email,
            }
        )

    state.discovery_results = results
    state.logs.append(
        f"DiscoveryAgent: discovered {len(results)} simulated locations for this user."
    )

    return state
