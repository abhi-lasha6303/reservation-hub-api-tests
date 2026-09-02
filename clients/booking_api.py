from clients.http_client import HttpClient
from config.settings import settings


class BookingApi:

    def __init__(self):
        self.http = HttpClient()

    # GET /ping
    def ping(self):
        return self.http.request(
            "GET",
            "/ping"
        )

    # POST /auth
    def create_token(self, username=None, password=None):
        payload = {
            "username": username if username is not None else settings.USERNAME,
            "password": password if password is not None else settings.PASSWORD
        }

        return self.http.request(
            "POST",
            "/auth",
            json=payload
        )

    # GET /booking
    def list_bookings(self, **filters):
        return self.http.request(
            "GET",
            "/booking",
            params=filters or None
        )

    # GET /booking/{id}
    def get_booking(self, booking_id):
        return self.http.request(
            "GET",
            f"/booking/{booking_id}"
        )

    # POST /booking
    def create_booking(self, payload):
        return self.http.request(
            "POST",
            "/booking",
            json=payload
        )

    # PUT /booking/{id}
    def update_booking(self, booking_id, payload, token=None):
        headers = self._auth_headers(token)

        return self.http.request(
            "PUT",
            f"/booking/{booking_id}",
            json=payload,
            headers=headers
        )

    # PATCH /booking/{id}
    def patch_booking(self, booking_id, payload, token=None):
        headers = self._auth_headers(token)

        return self.http.request(
            "PATCH",
            f"/booking/{booking_id}",
            json=payload,
            headers=headers
        )

    # DELETE /booking/{id}
    def delete_booking(self, booking_id, token=None):
        headers = self._auth_headers(token)

        return self.http.request(
            "DELETE",
            f"/booking/{booking_id}",
            headers=headers
        )

    @staticmethod
    def _auth_headers(token=None):
        if token:
            return {
                "Cookie": f"token={token}"
            }

        return {}