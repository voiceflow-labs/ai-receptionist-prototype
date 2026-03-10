import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
STAFF_NOTIFICATION_NUMBER = os.getenv("STAFF_NOTIFICATION_NUMBER")  # optional

def _get_client():
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise RuntimeError("Twilio credentials not configured in environment")
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_notification(body, to=None):
    """
    Send an SMS notification using Twilio. If `to` not provided, uses `STAFF_NOTIFICATION_NUMBER`.
    """
    to_number = to or STAFF_NOTIFICATION_NUMBER
    if not to_number:
        raise RuntimeError("No recipient number configured for notifications")
    client = _get_client()
    return client.messages.create(body=body, from_=TWILIO_PHONE_NUMBER, to=to_number)