from django.conf import settings

from customers.services.base_client import BaseServiceClient


class CartServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.CART_SERVICE_URL)

    def ensure(self, customer_id):
        return self.request("POST", "/carts/", json={"customer_id": customer_id})

    def get(self, customer_id):
        return self.request("GET", f"/carts/customer/{customer_id}/")

    def summary(self, customer_id):
        return self.request("GET", f"/carts/customer/{customer_id}/summary/")

    def add_item(self, customer_id, payload):
        return self.request("POST", f"/carts/customer/{customer_id}/items/", json=payload)

    def update_item(self, customer_id, item_id, payload):
        return self.request("PATCH", f"/carts/customer/{customer_id}/items/{item_id}/", json=payload)

    def delete_item(self, customer_id, item_id):
        return self.request("DELETE", f"/carts/customer/{customer_id}/items/{item_id}/")

    def clear(self, customer_id):
        return self.request("DELETE", f"/carts/customer/{customer_id}/clear/")
