from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import CartEnsureSerializer, CartItemCreateSerializer, CartItemSerializer, CartItemUpdateSerializer, CartSerializer
from .services.base_client import ServiceClientError
from .services.clothes_client import ClothesServiceClient
from .services.laptop_client import LaptopServiceClient


def api_response(*, data=None, message="Success", success=True, status_code=200):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def get_or_create_active_cart(customer_id):
    cart = Cart.objects.filter(customer_id=customer_id, status=Cart.Status.ACTIVE).first()
    if cart:
        return cart, False
    return Cart.objects.create(customer_id=customer_id), True


def fetch_product(product_type, product_id):
    if product_type == CartItem.ProductTypes.LAPTOP:
        return LaptopServiceClient().detail(product_id)
    return ClothesServiceClient().detail(product_id)


def cart_summary_payload(cart):
    items = list(cart.items.all())
    return {
        "cart_id": cart.id,
        "customer_id": cart.customer_id,
        "status": cart.status,
        "total_items": len(items),
        "total_quantity": sum(item.quantity for item in items),
        "total_amount": cart.total_amount,
        "items": CartItemSerializer(items, many=True).data,
    }


class CartEnsureView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = CartEnsureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, created = get_or_create_active_cart(serializer.validated_data["customer_id"])
        return api_response(
            message="Cart created successfully" if created else "Cart is ready",
            data=CartSerializer(cart).data,
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class CartByCustomerView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, customer_id):
        cart, _ = get_or_create_active_cart(customer_id)
        return api_response(message="Cart fetched successfully", data=CartSerializer(cart).data)


class CartSummaryView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, customer_id):
        cart, _ = get_or_create_active_cart(customer_id)
        return api_response(message="Cart summary fetched successfully", data=cart_summary_payload(cart))


class CartItemCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, customer_id):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = get_or_create_active_cart(customer_id)

        try:
            product = fetch_product(serializer.validated_data["product_type"], serializer.validated_data["product_id"])
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        quantity = serializer.validated_data["quantity"]
        if int(product["stock"]) < quantity:
            return api_response(
                message="Product does not have enough stock.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_type=serializer.validated_data["product_type"],
            product_id=serializer.validated_data["product_id"],
            defaults={
                "product_name": product["name"],
                "unit_price": product["price"],
                "quantity": quantity,
            },
        )
        if not created:
            item.quantity += quantity
            if int(product["stock"]) < item.quantity:
                return api_response(
                    message="Updated quantity exceeds current stock.",
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            item.product_name = product["name"]
            item.unit_price = product["price"]
            item.save()

        return api_response(
            message="Item added to cart successfully",
            data=CartItemSerializer(item).data,
            status_code=status.HTTP_201_CREATED,
        )


class CartItemDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def patch(self, request, customer_id, item_id):
        return self._update_item(request, customer_id, item_id)

    def put(self, request, customer_id, item_id):
        return self._update_item(request, customer_id, item_id)

    def _update_item(self, request, customer_id, item_id):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = get_or_create_active_cart(customer_id)
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if not item:
            return api_response(message="Cart item not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

        quantity = serializer.validated_data["quantity"]
        if quantity == 0:
            item.delete()
            return api_response(message="Cart item removed successfully", data=None)

        try:
            product = fetch_product(item.product_type, item.product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        if int(product["stock"]) < quantity:
            return api_response(
                message="Requested quantity exceeds stock.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        item.product_name = product["name"]
        item.unit_price = product["price"]
        item.quantity = quantity
        item.save()
        return api_response(message="Cart item updated successfully", data=CartItemSerializer(item).data)

    def delete(self, request, customer_id, item_id):
        cart, _ = get_or_create_active_cart(customer_id)
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if not item:
            return api_response(message="Cart item not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)
        item.delete()
        return api_response(message="Cart item deleted successfully", data=None)


class CartClearView(APIView):
    authentication_classes = []
    permission_classes = []

    def delete(self, request, customer_id):
        cart, _ = get_or_create_active_cart(customer_id)
        cart.items.all().delete()
        return api_response(message="Cart cleared successfully", data=cart_summary_payload(cart))
