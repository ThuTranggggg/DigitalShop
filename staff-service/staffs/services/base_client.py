import requests
from django.conf import settings
from requests import RequestException


class ServiceClientError(Exception):
    pass


class BaseServiceClient:
    timeout = getattr(settings, "SERVICE_TIMEOUT", 10)

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, path: str, *, params=None, json=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = requests.request(
                method,
                url,
                params=params,
                json=json,
                timeout=self.timeout,
            )
        except RequestException as exc:
            raise ServiceClientError(f"Service request failed: {exc}") from exc

        try:
            payload = response.json()
        except ValueError:
            payload = {"message": response.text or "Unknown service response"}

        if response.status_code >= 400:
            message = payload.get("message") or payload.get("detail") or "Service request failed"
            raise ServiceClientError(message)

        return payload.get("data", payload)
