"""
Test-data builders.

Every test builds its own booking rather than reusing a shared constant. Two
reasons:

* The sandbox is shared and resets roughly every ten minutes, so any test that
  relied on data it did not create itself would be order-dependent and flaky.
* Unique names let a test find its own booking through the search filters
  without colliding with the ten seeded records or with a parallel run.
"""

import uuid
from datetime import date, timedelta

REQUIRED_FIELDS = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]

DATE_FORMAT = "%Y-%m-%d"


def unique_suffix() -> str:
    """Short, collision-resistant token for building unique names."""
    return uuid.uuid4().hex[:8]


def iso_date(days_from_today: int) -> str:
    return (date.today() + timedelta(days=days_from_today)).strftime(DATE_FORMAT)


def build_booking(**overrides) -> dict:
    """Return a valid booking payload, with any field replaced by an override.

    `build_booking(totalprice=-500)` reads as "a normal booking, except the price
    is negative", which keeps the intent of each negative test visible on one
    line instead of buried in a wall of JSON.

    Passing `None` for a key removes it entirely -- that is how the
    missing-required-field cases are built.
    """
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
    """Sentinel meaning 'leave this field out of the payload entirely'.

    A plain `None` cannot be used, because `None` is itself a value worth
    testing -- "totalprice: null" and "no totalprice key" are different requests
    and a correct API may well answer them differently.
    """

    def __repr__(self) -> str:
        return "<OMIT>"


_OMIT = _Omit()
OMIT = _OMIT


def build_booking_without(field: str) -> dict:
    """A valid booking with one required field removed."""
    return build_booking(**{field: OMIT})


def build_dates(checkin_offset: int, checkout_offset: int) -> dict:
    return {
        "checkin": iso_date(checkin_offset),
        "checkout": iso_date(checkout_offset),
    }
