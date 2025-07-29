# calendar_storage.py
import os
import pickle
from datetime import datetime, date as _date, time as _time
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.pickle")
LOCAL_TZ = ZoneInfo(os.getenv("AGENT_TZ", "America/Chicago"))
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")


def _get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
    return build("calendar", "v3", credentials=creds)


def create_event(service: str, date: str, time: str) -> dict:
    """
    Create a Google Calendar event.
    Args:
      service: the booking summary
      date: 'YYYY-MM-DD'
      time: 'HH:MM'
    Returns:
      The created event resource.
    """
    # parse into datetime
    dt_date = _date.fromisoformat(date)
    dt_time = _time.fromisoformat(time)
    start_dt = datetime.combine(dt_date, dt_time, tzinfo=LOCAL_TZ)
    end_dt = start_dt  # zero‑length event, adjust if you need duration
    event = {
        "summary": service,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": LOCAL_TZ.key,
        },
        "end": {
            "dateTime": (start_dt).isoformat(),
            "timeZone": LOCAL_TZ.key,
        },
    }
    service = _get_calendar_service()
    created = service.events().insert(
        calendarId=CALENDAR_ID, body=event
    ).execute()
    return created
