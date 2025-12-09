# backend/app/agents/state.py

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


# -------------------------
# Helper Enum Types
# -------------------------

class IdentityStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"


class RequestType(str, Enum):
    DELETION = "deletion"
    ACCESS = "access"          # future
    RECTIFICATION = "rectification"  # future
    RESTRICTION = "restriction"      # future


class Mode(str, Enum):
    SIMULATION = "SIMULATION"
    LIVE = "LIVE"


class LocationType(str, Enum):
    SQL_ROW = "sql_row"
    MONGO_DOC = "mongo_doc"
    FILE = "file"


class ActionType(str, Enum):
    MASK = "mask"
    DELETE = "delete"
    FLAG = "flag"
    NONE = "none"  # in case nothing needed


class ActionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


# -------------------------
# Structured Helper Data
# -------------------------

@dataclass
class UserIdentifiers:
    email: Optional[str] = None
    customer_id: Optional[str] = None
    phone_last4: Optional[str] = None
    dob: Optional[str] = None  # keep as string "YYYY-MM-DD" for simplicity


@dataclass
class DataLocation:
    """
    Represents one place where the user's data was found.
    Example:
      - SQL row in customers table
      - Mongo document in events collection
      - JSON file in ADLS path
    """

    source_name: str                       # e.g., "CustomerDB", "MongoEvents", "ADLS_Customers"
    location_type: LocationType            # SQL_ROW / MONGO_DOC / FILE

    # SQL specific
    table_name: Optional[str] = None
    primary_key: Optional[str] = None      # store as string for simplicity

    # Mongo specific
    collection_name: Optional[str] = None
    document_id: Optional[str] = None

    # File specific
    file_path: Optional[str] = None

    # Which PII fields were detected here (e.g., ["email", "phone"])
    pii_fields: List[str] = field(default_factory=list)


@dataclass
class DeletionAction:
    """
    Represents what we did (or would do) to one DataLocation.
    """

    location: DataLocation
    action_type: ActionType                # mask / delete / flag
    status: ActionStatus                   # success / failed / skipped
    details: Optional[str] = None          # e.g., SQL query, file path, error message


# -------------------------
# Main State Object
# -------------------------

@dataclass
class RegentState:
    """
    This is the shared state flowing through all agents in the graph.
    Each node (agent) reads and updates this.
    """

    # Core request info
    request_id: Optional[int] = None
    request_type: Optional[RequestType] = None

    # Original user input (message/reason text)
    user_input: str = ""

    # Identity & verification
    user_identifiers: UserIdentifiers = field(default_factory=UserIdentifiers)
    identity_status: IdentityStatus = IdentityStatus.PENDING

    # Data discovery results (where we found the user)
    data_map: List[DataLocation] = field(default_factory=list)

    # Deletion/masking actions taken (or simulated)
    deletion_actions: List[DeletionAction] = field(default_factory=list)

    # Mode: SIMULATION or LIVE
    mode: Mode = Mode.SIMULATION

    # Logs to show step-by-step progress in UI
    logs: List[str] = field(default_factory=list)

    # Final summaries
    final_user_summary: str = ""
    final_admin_report: str = ""
