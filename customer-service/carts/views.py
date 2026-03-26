from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.permissions import IsCustomerUser
from customers.services.base_client import ServiceClientError

from .serializers import CartItemCreateSerializer, CartItemUpdateSerializer
from .services.cart_client import CartServiceClient


def api_response(*, data=None, message="Success", success=True, status_code=200):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


class CartView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        try:
            data = CartServiceClient().ensure(request.user.id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Cart is ready", data=data, status_code=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            data = CartServiceClient().get(request.user.id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Cart fetched successfully", data=data)


class CartItemCreateView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = CartServiceClient().add_item(request.user.id, serializer.validated_data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Item added to cart successfully", data=data, status_code=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def patch(self, request, item_id):
        return self._update(request, item_id)

    def put(self, request, item_id):
        return self._update(request, item_id)

    def _update(self, request, item_id):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = CartServiceClient().update_item(request.user.id, item_id, serializer.validated_data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        message = "Cart item removed successfully" if serializer.validated_data["quantity"] == 0 else "Cart item updated successfully"
        return api_response(message=message, data=data)

    def delete(self, request, item_id):
        try:
            CartServiceClient().delete_item(request.user.id, item_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Cart item deleted successfully", data=None)


class CartSummaryView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = CartServiceClient().summary(request.user.id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Cart summary fetched successfully", data=data)
