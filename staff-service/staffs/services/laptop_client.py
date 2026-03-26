from django.conf import settings

from .base_client import BaseServiceClient


class LaptopServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.LAPTOP_SERVICE_URL)

    def create_laptop(self, payload):
        return self.request("POST", "/laptops/", json=payload)

    def update_laptop(self, laptop_id, payload):
        return self.request("PUT", f"/laptops/{laptop_id}/", json=payload)

    def delete_laptop(self, laptop_id):
        return self.request("DELETE", f"/laptops/{laptop_id}/")

    def list_laptops(self, params=None):
        return self.request("GET", "/laptops/", params=params)

    def detail(self, product_id):
        return self.request("GET", f"/laptops/{product_id}/")

    def adjust_stock(self, product_id, quantity_delta):
        return self.request("POST", f"/laptops/{product_id}/stock-adjust/", json={"quantity_delta": quantity_delta})
