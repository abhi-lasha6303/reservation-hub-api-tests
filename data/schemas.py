"""
Response contracts, expressed as JSON Schema.

These describe the shape a *partner integration* depends on: which keys exist and
what type each one holds. Field-level value assertions stay in the tests; this
file answers the different question of whether the response is still the same
shape it was last release.

`additionalProperties` is left permissive on purpose -- a new optional field is a
backwards-compatible change and should not fail a regression suite. A missing
field or a changed type is not, and will.
"""

BOOKING_DATES_SCHEMA = {
    "type": "object",
    "required": ["checkin", "checkout"],
    "properties": {
        "checkin": {"type": "string"},
        "checkout": {"type": "string"},
    },
}

BOOKING_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": BOOKING_DATES_SCHEMA,
        "additionalneeds": {"type": "string"},
    },
}

CREATE_BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA,
    },
}

BOOKING_ID_LIST_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["bookingid"],
        "properties": {"bookingid": {"type": "integer"}},
    },
}

AUTH_TOKEN_SCHEMA = {
    "type": "object",
    "required": ["token"],
    "properties": {"token": {"type": "string", "minLength": 1}},
}
