# backend/app/agents/deletion_agent.py

from app.agents.state import (
    RegentState,
    DeletionAction,
    ActionType,
    ActionStatus,
    LocationType,
)
from app.tools.policy_engine import decide_action_for_location


def run_deletion_agent(state: RegentState) -> RegentState:
    """
    Deletion Agent (policy-driven simulation):

    - For each DataLocation in state.data_map:
        * Ask policy_engine.decide_action_for_location(location)
        * Build a DeletionAction using the returned ActionType + policy reason.
    - We do NOT actually modify any data yet (simulation only).
    """

    if not state.data_map:
        state.logs.append(
            "DeletionAgent: No data locations in state.data_map. Nothing to delete/mask/flag."
        )
        return state

    for loc in state.data_map:
        # Get action + reason from policy engine
        action_type, policy_reason = decide_action_for_location(loc)

        # Build nice description depending on location type
        if loc.location_type == LocationType.SQL_ROW:
            target_desc = (
                f"SQL table '{loc.table_name}', primary_key={loc.primary_key}"
            )
        elif loc.location_type == LocationType.MONGO_DOC:
            target_desc = (
                f"Mongo collection '{loc.collection_name}', document_id={loc.document_id}"
            )
        elif loc.location_type == LocationType.FILE:
            target_desc = f"File at path '{loc.file_path}'"
        else:
            target_desc = "Unknown location type"

        details = (
            f"Policy decision: {action_type.value.upper()} "
            f"(reason: {policy_reason}). "
            f"Target: source={loc.source_name}, {target_desc}, pii_fields={loc.pii_fields}"
        )

        deletion_action = DeletionAction(
            location=loc,
            action_type=action_type,
            status=ActionStatus.SUCCESS,
            details=details,
        )

        state.deletion_actions.append(deletion_action)

    state.logs.append(
        f"DeletionAgent: Created {len(state.deletion_actions)} policy-driven simulated actions."
    )

    return state
