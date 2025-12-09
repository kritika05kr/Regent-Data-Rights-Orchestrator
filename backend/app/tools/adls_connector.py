# backend/app/tools/adls_connector.py

import os
from typing import Optional, List

from app.core.config import get_settings
from app.agents.state import DataLocation, LocationType

settings = get_settings()


def search_user_pii_in_adls(
    email: Optional[str],
    customer_id: Optional[str],
) -> List[DataLocation]:
    """
    Discovery helper for ADLS-like storage (simulated with a local folder).

    We walk through all files under settings.ADLS_BASE_PATH and look for the
    email or customer_id as plain text inside .txt or .json files.

    If a match is found, we create a DataLocation with location_type=FILE.
    """

    locations: List[DataLocation] = []

    base_path = settings.ADLS_BASE_PATH
    if not base_path or not os.path.isdir(base_path):
        # Nothing configured / folder doesn't exist -> no results
        return locations

    # Nothing to search with
    if not email and not customer_id:
        return locations

    for root, _, files in os.walk(base_path):
        for filename in files:
            # Only scan text-like files for demo
            if not (filename.endswith(".txt") or filename.endswith(".json")):
                continue

            full_path = os.path.join(root, filename)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                print(f"[ADLSConnector] Could not read file {full_path}: {e}")
                continue

            matched_fields = []

            if email and email in content:
                matched_fields.append("email")
            if customer_id and customer_id in content:
                matched_fields.append("customer_id")

            if matched_fields:
                loc = DataLocation(
                    source_name="ADLS",
                    location_type=LocationType.FILE,
                    file_path=full_path,
                    pii_fields=matched_fields,
                )
                locations.append(loc)

    return locations
