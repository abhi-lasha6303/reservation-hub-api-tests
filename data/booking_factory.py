import uuid
from datetime import date, timedelta

REQUIRED_FIELDS = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]

DATE_FORMAT = "%Y-%m-%d"


def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]


def iso_date(days_from_today: int) -> str:
    return (date.today() + timedelta(days=days_from_today)).strftime(DATE_FORMAT)


def build_booking(**overrides) -> dict:
    booking = {
        "firstname": f"Test{unique_suffix()}",
        "lastname": f"Booking{unique_suffix()}",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": iso_date(7),
            "checkout": iso_date(10),
        },
        "additionalneeds": "Breakfast",
    }

    for key, value in overrides.items():
        if value is _OMIT:
            booking.pop(key, None)
        else:
            booking[key] = value

    return booking


class _Omit:

    def __repr__(self) -> str:
        return "<OMIT>"


_OMIT = _Omit()
OMIT = _OMIT


def build_booking_without(field: str) -> dict:
    return build_booking(**{field: OMIT})


def build_dates(checkin_offset: int, checkout_offset: int) -> dict:
    return {
        "checkin": iso_date(checkin_offset),
        "checkout": iso_date(checkout_offset),
    }