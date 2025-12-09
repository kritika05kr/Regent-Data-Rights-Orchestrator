# backend/app/tools/sql_connector.py

from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.models.user_profile import UserProfile
from app.db.models.customer_order import CustomerOrder
from app.agents.state import DataLocation, LocationType


def get_user_profile_by_identifiers(
    db: Session,
    email: Optional[str] = None,
    customer_id: Optional[str] = None,
    phone_last4: Optional[str] = None,
) -> Optional[UserProfile]:
    """
    Look up a user in the UserProfile table using available identifiers.
    """

    query = db.query(UserProfile)

    if email:
        query = query.filter(UserProfile.email == email)
    elif customer_id:
        query = query.filter(UserProfile.customer_id == customer_id)
    elif phone_last4:
        like_pattern = f"%{phone_last4}"
        query = query.filter(UserProfile.phone.like(like_pattern))
    else:
        return None

    return query.first()


def search_user_pii_in_sql(
    db: Session,
    email: Optional[str],
    customer_id: Optional[str],
) -> List[DataLocation]:
    """
    Discovery helper:
    - Find all rows in CustomerOrder that belong to this user
      by email or customer_id.
    - Return them as DataLocation objects.
    """

    query = db.query(CustomerOrder)

    if email:
        query = query.filter(CustomerOrder.user_email == email)
    if customer_id:
        query = query.filter(CustomerOrder.customer_id == customer_id)

    rows = query.all()
    locations: List[DataLocation] = []

    for row in rows:
        loc = DataLocation(
            source_name="CustomerDB",
            location_type=LocationType.SQL_ROW,
            table_name="customer_orders",
            primary_key=str(row.id),
            pii_fields=["user_email", "customer_id", "shipping_address", "notes"],
        )
        locations.append(loc)

    return locations
