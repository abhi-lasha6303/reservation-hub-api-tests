import pytest


@pytest.mark.health
def test_ping(api):
    response = api.ping()

    assert response.status_code == 201
    assert response.text == "Created"