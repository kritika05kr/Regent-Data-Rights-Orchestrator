# backend/app/tools/policy_engine.py

from dataclasses import dataclass
from typing import List, Optional, Tuple

from app.agents.state import DataLocation, LocationType, ActionType


@dataclass
class PolicyRule:
    """
    Simple policy rule.

    You can match on:
      - source_name (e.g. "CustomerDB", "MongoEvents", "ADLS")
      - location_type (SQL_ROW / MONGO_DOC / FILE)

    And decide:
      - which ActionType to use: MASK / DELETE / FLAG

    description: human-readable explanation for audit logs.
    """

    source_name: Optional[str] = None
    location_type: Optional[LocationType] = None
    action: ActionType = ActionType.MASK
    description: str = ""


# ----------------------------------------------------------------------
# Example policy rules (you can customize/extend later)
# ----------------------------------------------------------------------

POLICY_RULES: List[PolicyRule] = [
    PolicyRule(
        source_name="CustomerDB",
        location_type=LocationType.SQL_ROW,
        action=ActionType.MASK,
        description="Mask user PII in transactional SQL systems instead of hard delete.",
    ),
    PolicyRule(
        source_name="MongoEvents",
        location_type=LocationType.MONGO_DOC,
        action=ActionType.DELETE,
        description="Delete event documents from Mongo to minimize long-term tracking.",
    ),
    PolicyRule(
        source_name="ADLS",
        location_type=LocationType.FILE,
        action=ActionType.FLAG,
        description="Flag files in ADLS for manual review due to unstructured content.",
    ),
]


def decide_action_for_location(location: DataLocation) -> Tuple[ActionType, str]:
    """
    Given a DataLocation, find the first matching policy rule.

    Matching logic:
      - First rule where (source_name matches OR is None) AND (location_type matches OR is None)
      - If no rule matches, default to MASK with generic description.

    Returns:
      (action_type, policy_reason)
    """

    for rule in POLICY_RULES:
        # Check source_name match (if rule specifies it)
        if rule.source_name is not None and rule.source_name != location.source_name:
            continue

        # Check location_type match (if rule specifies it)
        if rule.location_type is not None and rule.location_type != location.location_type:
            continue

        # Rule matches
        return rule.action, rule.description or "Matched policy rule."

    # Default policy: MASK
    return ActionType.MASK, "Default policy: mask PII when no specific rule is defined."
