import pytest


@pytest.mark.search
def test_list_bookings(api):
    response = api.list_bookings()

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    for booking in body:
        assert isinstance(booking, dict)
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)


@pytest.mark.search
def test_list_bookings_by_firstname(api, created_booking):
    firstname = created_booking["payload"]["firstname"]

    response = api.list_bookings(
        firstname=firstname
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    assert any(
        item["bookingid"] == created_booking["id"]
        for item in body
    )


@pytest.mark.search
def test_list_bookings_by_lastname(api, created_booking):
    lastname = created_booking["payload"]["lastname"]

    response = api.list_bookings(
        lastname=lastname
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    assert any(
        item["bookingid"] == created_booking["id"]
        for item in body
    )


@pytest.mark.search
def test_list_bookings_by_checkin(api, created_booking):
    checkin = created_booking["payload"]["bookingdates"]["checkin"]

    response = api.list_bookings(
        checkin=checkin
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)


@pytest.mark.search
def test_list_bookings_by_checkout(api, created_booking):
    checkout = created_booking["payload"]["bookingdates"]["checkout"]

    response = api.list_bookings(
        checkout=checkout
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)