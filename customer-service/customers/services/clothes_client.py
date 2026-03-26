from django.conf import settings

from .base_client import BaseServiceClient


class ClothesServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.CLOTHES_SERVICE_URL)

    def list(self, params=None):
        return self.request("GET", "/clothes/", params=params)

    def search(self, params=None):
        return self.request("GET", "/clothes/search/", params=params)

    def detail(self, product_id):
        return self.request("GET", f"/clothes/{product_id}/")

    def adjust_stock(self, product_id, quantity_delta):
        return self.request("POST", f"/clothes/{product_id}/stock-adjust/", json={"quantity_delta": quantity_delta})
