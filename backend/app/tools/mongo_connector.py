# backend/app/tools/mongo_connector.py

from typing import Optional, List

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.core.config import get_settings
from app.agents.state import DataLocation, LocationType

settings = get_settings()


def search_user_pii_in_mongo(
    email: Optional[str],
    customer_id: Optional[str],
) -> List[DataLocation]:
    """
    Discovery helper for MongoDB.

    Assumes there is a collection named "events" that stores user-related events,
    with fields like:
        - "email"
        - "customer_id"
        - "payload" (may contain PII text)

    This function:
      - Connects to MongoDB using settings.MONGO_URI / MONGO_DB_NAME
      - Builds a query using available identifiers
      - Returns DataLocation objects for matching documents

    If Mongo is not available, it catches the error and returns an empty list
    so the system continues working.
    """

    locations: List[DataLocation] = []

    # Nothing to search with
    if not email and not customer_id:
        return locations

    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        collection = db["events"]

        query = {}
        if email:
            query["email"] = email
        if customer_id:
            query["customer_id"] = customer_id

        # Limit to a reasonable number for demo
        cursor = collection.find(query).limit(50)

        for doc in cursor:
            loc = DataLocation(
                source_name="MongoEvents",
                location_type=LocationType.MONGO_DOC,
                collection_name="events",
                document_id=str(doc.get("_id")),
                pii_fields=["email", "customer_id", "payload"],
            )
            locations.append(loc)

        client.close()
    except PyMongoError as e:
        # If Mongo is not running or any error occurs, just log and return empty.
        print(f"[MongoConnector] Error while searching MongoDB: {e}")
    except Exception as e:
        print(f"[MongoConnector] Unexpected error: {e}")

    return locations
