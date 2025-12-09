from typing import Any, List, Dict


class PolicyAgent:
    """
    Takes discovery results and decides policy actions for each location.

    - Input: state.discovery_results (list of dicts)
    - Output:
        - state.deletion_actions (list of dicts)
        - state.status updated (COMPLETED / PARTIAL)
    """

    def run(self, state: Any) -> Any:
        discovery_results = getattr(state, "discovery_results", []) or []
        actions: List[Dict] = []

        if not discovery_results:
            state.logs.append(
                "PolicyAgent: no discovery results, nothing to delete/mask/flag."
            )
            state.deletion_actions = []
            # For demo, still mark as completed
            state.status = "COMPLETED"
            return state

        had_failure = False

        for hit in discovery_results:
            if isinstance(hit, dict):
                source = hit.get("source", "unknown_source")
                location_type = hit.get("location_type", "unknown_location")
                pii_type = hit.get("pii_type", "generic_pii")
                identifier = hit.get("identifier", "")
            else:
                source = getattr(hit, "source", "unknown_source")
                location_type = getattr(hit, "location_type", "unknown_location")
                pii_type = getattr(hit, "pii_type", "generic_pii")
                identifier = getattr(hit, "identifier", "")

            # Simple rule:
            # - If pii_type contains "email" or "phone" => MASK
            # - otherwise => FLAG
            pii_str = str(pii_type).lower()
            if "email" in pii_str or "phone" in pii_str:
                action_type = "MASK"
            else:
                action_type = "FLAG"

            action_status = "SIMULATED_OK"

            details_parts = [f"pii_type={pii_type}"]
            if identifier:
                details_parts.append(f"identifier={identifier}")
            details = "; ".join(details_parts)

            actions.append(
                {
                    "source_name": source,
                    "location_type": location_type,
                    "action_type": action_type,
                    "status": action_status,
                    "details": details,
                }
            )

        state.deletion_actions = actions

        if had_failure:
            state.status = "PARTIAL"
            state.logs.append(
                "PolicyAgent: some actions failed → marking status PARTIAL."
            )
        else:
            state.status = "COMPLETED"
            state.logs.append(
                f"PolicyAgent: generated {len(actions)} simulated actions → status COMPLETED."
            )

        return state


def run_policy_agent(state: Any) -> Any:
    agent = PolicyAgent()
    return agent.run(state)
