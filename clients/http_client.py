import requests

from config.settings import settings


class HttpClient:

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.request_history = []

    def clear_history(self):
        self.request_history.clear()

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"

        response = requests.request(
            method=method,
            url=url,
            timeout=settings.TIMEOUT,
            **kwargs
        )

        self.request_history.append({
            "method": method,
            "url": url,
            "request_body": kwargs.get("json"),
            "request_params": kwargs.get("params"),
            "response_status": response.status_code,
            "response_body": response.text
        })

        return response