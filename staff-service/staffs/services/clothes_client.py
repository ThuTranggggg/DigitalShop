from django.conf import settings

from .base_client import BaseServiceClient


class ClothesServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.CLOTHES_SERVICE_URL)

    def create_clothes(self, payload):
        return self.request("POST", "/clothes/", json=payload)

    def update_clothes(self, product_id, payload):
        return self.request("PUT", f"/clothes/{product_id}/", json=payload)

    def delete_clothes(self, product_id):
        return self.request("DELETE", f"/clothes/{product_id}/")

    def list_clothes(self, params=None):
        return self.request("GET", "/clothes/", params=params)

    def detail(self, product_id):
        return self.request("GET", f"/clothes/{product_id}/")

    def adjust_stock(self, product_id, quantity_delta):
        return self.request("POST", f"/clothes/{product_id}/stock-adjust/", json={"quantity_delta": quantity_delta})
