# backend/seed_users.py

import os
import sys
from datetime import date, datetime

# Ensure "app" package is importable when running this as a script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models.user_profile import UserProfile
from app.db.models.customer_order import CustomerOrder


def seed():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Clear existing rows for a clean demo
        db.query(CustomerOrder).delete()
        db.query(UserProfile).delete()

        # ----- Seed users -----
        users = [
            UserProfile(
                email="kritika@example.com",
                customer_id="CUST001",
                phone="9999912345",
                dob=date(2002, 1, 15),
                full_name="Kritika Kumari",
            ),
            UserProfile(
                email="alice@example.com",
                customer_id="CUST002",
                phone="8888856789",
                dob=date(1995, 5, 20),
                full_name="Alice Wonderland",
            ),
            UserProfile(
                email="bob@example.com",
                customer_id="CUST003",
                phone="7777767890",
                dob=date(1990, 7, 10),
                full_name="Bob Builder",
            ),
        ]
        db.add_all(users)
        db.commit()

        # ----- Seed orders (PII) -----
        orders = [
            CustomerOrder(
                user_email="kritika@example.com",
                customer_id="CUST001",
                order_number="ORD-1001",
                shipping_address="221B Baker Street, London",
                notes="Leave at door",
                created_at=datetime.utcnow(),
            ),
            CustomerOrder(
                user_email="kritika@example.com",
                customer_id="CUST001",
                order_number="ORD-1002",
                shipping_address="221B Baker Street, London",
                notes="Handle with care",
                created_at=datetime.utcnow(),
            ),
            CustomerOrder(
                user_email="alice@example.com",
                customer_id="CUST002",
                order_number="ORD-2001",
                shipping_address="Wonderland Lane",
                notes="Gift wrap",
                created_at=datetime.utcnow(),
            ),
        ]
        db.add_all(orders)
        db.commit()

        print("✅ Seeded sample users and customer orders.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
