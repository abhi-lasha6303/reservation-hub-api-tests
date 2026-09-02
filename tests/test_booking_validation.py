import pytest


# ---------------------------------------------------------------------------
# Missing required fields
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.critical
@pytest.mark.parametrize(
    "payload",
    [
        {
            # firstname is missing
            "lastname": "Tester",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-09-10",
                "checkout": "2026-09-15"
            }
        },
        {
            # lastname is missing
            "firstname": "Abhi",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-09-10",
                "checkout": "2026-09-15"
            }
        },
        {
            # firstname and lastname are both missing
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-09-10",
                "checkout": "2026-09-15"
            }
        }
    ]
)
def test_create_booking_missing_required_field(api, payload):
    response = api.create_booking(payload)

    assert response.status_code in (400, 422), (
        "API should reject a booking when required fields are missing. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Invalid / boundary prices
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.critical
@pytest.mark.parametrize(
    "price",
    [
        0,
        -1,
        -100
    ]
)
def test_create_booking_invalid_price(api, booking_payload, price):
    payload = booking_payload.copy()
    payload["totalprice"] = price

    response = api.create_booking(payload)

    assert response.status_code in (400, 422), (
        f"API should reject invalid totalprice={price}. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Wrong price data types
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.parametrize(
    "price",
    [
        "100",
        "one hundred",
        None,
        []
    ]
)
def test_create_booking_wrong_price_type(api, booking_payload, price):
    payload = booking_payload.copy()
    payload["totalprice"] = price

    response = api.create_booking(payload)

    assert response.status_code in (400, 422), (
        f"API should reject invalid totalprice type/value: {price!r}. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Empty payload
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.critical
def test_create_booking_empty_payload(api):
    response = api.create_booking({})

    assert response.status_code in (400, 422), (
        "API should reject an empty booking payload. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Invalid booking date order
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.critical
def test_create_booking_checkout_before_checkin(api, booking_payload):
    payload = booking_payload.copy()

    payload["bookingdates"] = {
        "checkin": "2026-09-20",
        "checkout": "2026-09-10"
    }

    response = api.create_booking(payload)

    assert response.status_code in (400, 422), (
        "API should reject checkout dates earlier than check-in dates. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Malformed dates
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.parametrize(
    "checkin, checkout",
    [
        ("10-09-2026", "15-09-2026"),
        ("2026/09/10", "2026/09/15"),
        ("invalid-date", "2026-09-15"),
        ("2026-09-10", "invalid-date"),
        ("", "2026-09-15")
    ]
)
def test_create_booking_malformed_dates(
    api,
    booking_payload,
    checkin,
    checkout
):
    payload = booking_payload.copy()

    payload["bookingdates"] = {
        "checkin": checkin,
        "checkout": checkout
    }

    response = api.create_booking(payload)

    assert response.status_code in (400, 422), (
        f"API should reject malformed dates. "
        f"Check-in: {checkin!r}, Checkout: {checkout!r}. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Wrong firstname data types
# ---------------------------------------------------------------------------

@pytest.mark.create
@pytest.mark.parametrize(
    "firstname",
    [
        123,
        True,
        [],
        {}
    ]
)
def test_create_booking_wrong_firstname_type(
    api,
    booking_payload,
    firstname
):
    payload = booking_payload.copy()
    payload["firstname"] = firstname

    response = api.create_booking(payload)

    assert response.status_code in (400, 422), (
        f"API should reject invalid firstname type/value: {firstname!r}. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


# ---------------------------------------------------------------------------
# Non-existent / boundary booking IDs
# ---------------------------------------------------------------------------

@pytest.mark.read
def test_get_nonexistent_booking(api):
    response = api.get_booking(999999999)

    assert response.status_code == 404, (
        f"Expected 404 for a non-existent booking ID. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


@pytest.mark.read
def test_get_booking_zero_id(api):
    response = api.get_booking(0)

    assert response.status_code == 404, (
        f"Expected 404 for booking ID 0. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )


@pytest.mark.read
def test_get_booking_negative_id(api):
    response = api.get_booking(-1)

    assert response.status_code == 404, (
        f"Expected 404 for negative booking ID. "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )