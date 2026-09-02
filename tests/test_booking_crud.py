import pytest


@pytest.mark.create
@pytest.mark.critical
def test_create_booking(api, booking_payload):
    response = api.create_booking(booking_payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert "bookingid" in body
    assert "booking" in body

    assert isinstance(body["bookingid"], int)

    booking = body["booking"]

    assert booking["firstname"] == booking_payload["firstname"]
    assert booking["lastname"] == booking_payload["lastname"]
    assert booking["totalprice"] == booking_payload["totalprice"]
    assert booking["depositpaid"] == booking_payload["depositpaid"]

    assert booking["bookingdates"]["checkin"] == (
        booking_payload["bookingdates"]["checkin"]
    )

    assert booking["bookingdates"]["checkout"] == (
        booking_payload["bookingdates"]["checkout"]
    )


@pytest.mark.read
def test_get_created_booking(api, created_booking):
    booking_id = created_booking["id"]
    expected = created_booking["payload"]

    response = api.get_booking(booking_id)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body["firstname"] == expected["firstname"]
    assert body["lastname"] == expected["lastname"]
    assert body["totalprice"] == expected["totalprice"]
    assert body["depositpaid"] == expected["depositpaid"]

    assert body["bookingdates"]["checkin"] == (
        expected["bookingdates"]["checkin"]
    )

    assert body["bookingdates"]["checkout"] == (
        expected["bookingdates"]["checkout"]
    )


@pytest.mark.update
@pytest.mark.critical
def test_put_booking(api, created_booking, auth_token):
    booking_id = created_booking["id"]

    updated_payload = {
        "firstname": "Updated",
        "lastname": "PUTUser",
        "totalprice": 250,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-10-01",
            "checkout": "2026-10-10"
        },
        "additionalneeds": "Lunch"
    }

    response = api.update_booking(
        booking_id,
        updated_payload,
        auth_token
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body["firstname"] == "Updated"
    assert body["lastname"] == "PUTUser"
    assert body["totalprice"] == 250
    assert body["depositpaid"] is False

    assert body["bookingdates"]["checkin"] == "2026-10-01"
    assert body["bookingdates"]["checkout"] == "2026-10-10"

    assert body["additionalneeds"] == "Lunch"


@pytest.mark.update
def test_patch_booking(api, created_booking, auth_token):
    booking_id = created_booking["id"]

    patch_payload = {
        "firstname": "Patched"
    }

    response = api.patch_booking(
        booking_id,
        patch_payload,
        auth_token
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body["firstname"] == "Patched"


@pytest.mark.delete
@pytest.mark.critical
def test_delete_booking(api, created_booking, auth_token):
    booking_id = created_booking["id"]

    response = api.delete_booking(
        booking_id,
        auth_token
    )

    assert response.status_code == 201
    assert response.text == "Created"

    get_response = api.get_booking(booking_id)

    assert get_response.status_code == 404