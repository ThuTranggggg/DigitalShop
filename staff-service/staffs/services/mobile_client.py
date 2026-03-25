from django.conf import settings

from .base_client import BaseServiceClient


class MobileServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.MOBILE_SERVICE_URL)

    def create_mobile(self, payload):
        return self.request("POST", "/mobiles/", json=payload)

    def update_mobile(self, mobile_id, payload):
        return self.request("PUT", f"/mobiles/{mobile_id}/", json=payload)

    def delete_mobile(self, mobile_id):
        return self.request("DELETE", f"/mobiles/{mobile_id}/")

    def list_mobiles(self, params=None):
        return self.request("GET", "/mobiles/", params=params)
