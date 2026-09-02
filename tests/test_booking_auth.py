import pytest


@pytest.mark.auth
def test_put_without_auth(api, created_booking):
    booking_id = created_booking["id"]

    payload = {
        "firstname": "NoAuth",
        "lastname": "User",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-11-01",
            "checkout": "2026-11-05"
        },
        "additionalneeds": "Breakfast"
    }

    response = api.update_booking(
        booking_id,
        payload
    )

    assert response.status_code == 403


@pytest.mark.auth
def test_put_with_invalid_auth(api, created_booking):
    booking_id = created_booking["id"]

    payload = {
        "firstname": "InvalidAuth",
        "lastname": "User",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-11-01",
            "checkout": "2026-11-05"
        },
        "additionalneeds": "Breakfast"
    }

    response = api.update_booking(
        booking_id,
        payload,
        token="invalid-token"
    )

    assert response.status_code == 403


@pytest.mark.auth
def test_patch_without_auth(api, created_booking):
    booking_id = created_booking["id"]

    response = api.patch_booking(
        booking_id,
        {"firstname": "NoAuth"}
    )

    assert response.status_code == 403


@pytest.mark.auth
def test_patch_with_invalid_auth(api, created_booking):
    booking_id = created_booking["id"]

    response = api.patch_booking(
        booking_id,
        {"firstname": "InvalidAuth"},
        token="invalid-token"
    )

    assert response.status_code == 403


@pytest.mark.auth
def test_delete_without_auth(api, created_booking):
    booking_id = created_booking["id"]

    response = api.delete_booking(booking_id)

    assert response.status_code == 403


@pytest.mark.auth
def test_delete_with_invalid_auth(api, created_booking):
    booking_id = created_booking["id"]

    response = api.delete_booking(
        booking_id,
        token="invalid-token"
    )

    assert response.status_code == 403