# backend/app/services/notification_service.py

"""
Optional notification helpers.

Right now it's just a stub. In future you can integrate:
- SMTP email
- SendGrid
- Slack/Teams webhooks
"""

def send_user_email(email: str, subject: str, body: str) -> None:
    # For now, we just print to console.
    print(f"[EMAIL to {email}] {subject}\n{body}\n")
