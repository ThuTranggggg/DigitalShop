from django.conf import settings

from .base_client import BaseServiceClient


class MobileServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.MOBILE_SERVICE_URL)

    def list(self, params=None):
        return self.request("GET", "/mobiles/", params=params)

    def search(self, params=None):
        return self.request("GET", "/mobiles/search/", params=params)

    def detail(self, product_id):
        return self.request("GET", f"/mobiles/{product_id}/")
