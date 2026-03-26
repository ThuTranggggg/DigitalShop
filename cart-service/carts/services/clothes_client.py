from django.conf import settings

from .base_client import BaseServiceClient


class ClothesServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.CLOTHES_SERVICE_URL)

    def detail(self, product_id):
        return self.request("GET", f"/clothes/{product_id}/")
