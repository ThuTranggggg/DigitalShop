from django.conf import settings

from .base_client import BaseServiceClient


class LaptopServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.LAPTOP_SERVICE_URL)

    def detail(self, product_id):
        return self.request("GET", f"/laptops/{product_id}/")
