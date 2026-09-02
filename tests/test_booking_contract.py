import pytest
from jsonschema import validate


CREATE_BOOKING_SCHEMA = {
    "type": "object",
    "required": [
        "bookingid",
        "booking"
    ],
    "properties": {
        "bookingid": {
            "type": "integer"
        },
        "booking": {
            "type": "object",
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates"
            ],
            "properties": {
                "firstname": {
                    "type": "string"
                },
                "lastname": {
                    "type": "string"
                },
                "totalprice": {
                    "type": "integer"
                },
                "depositpaid": {
                    "type": "boolean"
                },
                "bookingdates": {
                    "type": "object",
                    "required": [
                        "checkin",
                        "checkout"
                    ],
                    "properties": {
                        "checkin": {
                            "type": "string"
                        },
                        "checkout": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}


BOOKING_SCHEMA = {
    "type": "object",
    "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates"
    ],
    "properties": {
        "firstname": {
            "type": "string"
        },
        "lastname": {
            "type": "string"
        },
        "totalprice": {
            "type": "integer"
        },
        "depositpaid": {
            "type": "boolean"
        },
        "bookingdates": {
            "type": "object",
            "required": [
                "checkin",
                "checkout"
            ],
            "properties": {
                "checkin": {
                    "type": "string"
                },
                "checkout": {
                    "type": "string"
                }
            }
        }
    }
}


@pytest.mark.contract
def test_create_booking_response_contract(api, booking_payload):
    response = api.create_booking(booking_payload)

    assert response.status_code == 200

    body = response.json()

    validate(
        instance=body,
        schema=CREATE_BOOKING_SCHEMA
    )


@pytest.mark.contract
def test_get_booking_response_contract(api, created_booking):
    booking_id = created_booking["id"]

    response = api.get_booking(booking_id)

    assert response.status_code == 200

    body = response.json()

    validate(
        instance=body,
        schema=BOOKING_SCHEMA
    )