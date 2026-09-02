import json
import pytest
import pytest_html

from clients.booking_api import BookingApi


@pytest.fixture(scope="session")
def api():
    return BookingApi()


@pytest.fixture(scope="session")
def auth_token(api):
    response = api.create_token()

    assert response.status_code == 200, (
        f"Authentication failed. "
        f"Status: {response.status_code}, "
        f"Body: {response.text}"
    )

    token = response.json().get("token")

    assert token, "Authentication response did not contain a token."

    return token


@pytest.fixture
def booking_payload():
    return {
        "firstname": "Abhi",
        "lastname": "Tester",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-10",
            "checkout": "2026-09-15"
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture
def created_booking(api, booking_payload):
    response = api.create_booking(booking_payload)

    assert response.status_code == 200, (
        f"Booking creation failed. "
        f"Status: {response.status_code}, "
        f"Body: {response.text}"
    )

    body = response.json()

    booking_id = body.get("bookingid")

    assert booking_id is not None, (
        "Create booking response does not contain bookingid."
    )

    return {
        "id": booking_id,
        "payload": booking_payload,
        "response": response
    }


# ---------------------------------------------------------------------------
# HTML report: attach API request/response details
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    api = item.funcargs.get("api")

    if api is None:
        return

    history = api.http.request_history

    if not history:
        return

    extras = getattr(report, "extras", [])

    for index, entry in enumerate(history, start=1):
        request_details = {
            "method": entry["method"],
            "url": entry["url"],
            "body": entry["request_body"],
            "params": entry["request_params"]
        }

        response_details = {
            "status": entry["response_status"],
            "body": entry["response_body"]
        }

        extras.append(
            pytest_html.extras.text(
                json.dumps(
                    request_details,
                    indent=2,
                    default=str
                ),
                name=f"Request {index}"
            )
        )

        extras.append(
            pytest_html.extras.text(
                json.dumps(
                    response_details,
                    indent=2,
                    default=str
                ),
                name=f"Response {index}"
            )
        )

    report.extras = extras