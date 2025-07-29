# booking_storage.py
from __future__ import annotations
import json, os, uuid
from typing import TypedDict, List
from datetime import date as _date, time as _time, datetime
from zoneinfo import ZoneInfo

BOOKINGS_PATH = os.getenv("BOOKINGS_PATH", "bookings.json")
LOCAL_TZ = ZoneInfo(os.getenv("AGENT_TZ", "America/Chicago"))

class Booking(TypedDict):
    id: str
    service: str
    date: str        # YYYY-MM-DD
    time: str        # HH:MM (24h, local)
    iso_start: str   # Full ISO-8601 with timezone

def _load_all() -> List[Booking]:
    if not os.path.exists(BOOKINGS_PATH):
        return []
    with open(BOOKINGS_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return list(data) if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def _save_all(items: List[Booking]) -> None:
    os.makedirs(os.path.dirname(BOOKINGS_PATH) or ".", exist_ok=True)
    with open(BOOKINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

def store_booking(service: str, date: str, time: str) -> Booking:
    # Validate normalised inputs
    try:
        d = _date.fromisoformat(date)          # YYYY-MM-DD
        t = _time.fromisoformat(time)          # HH:MM[:SS]
    except ValueError as e:
        raise ValueError(f"Invalid date/time format: {e}")

    start = datetime.combine(d, t, tzinfo=LOCAL_TZ)
    booking: Booking = {
        "id": str(uuid.uuid4()),
        "service": service.strip(),
        "date": d.isoformat(),
        "time": t.strftime("%H:%M"),
        "iso_start": start.isoformat(),
    }
    items = _load_all()
    items.append(booking)
    _save_all(items)
    return booking
