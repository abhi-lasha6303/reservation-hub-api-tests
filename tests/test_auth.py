import pytest


@pytest.mark.auth
def test_authentication_success(api):
    response = api.create_token()

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert "token" in body
    assert isinstance(body["token"], str)
    assert body["token"]


@pytest.mark.auth
def test_authentication_invalid_credentials(api):
    response = api.create_token(
        username="invalid-user",
        password="invalid-password"
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body.get("reason") == "Bad credentials"