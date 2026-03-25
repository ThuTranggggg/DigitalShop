from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.permissions import IsCustomerUser
from customers.services.base_client import ServiceClientError
from customers.services.laptop_client import LaptopServiceClient
from customers.services.mobile_client import MobileServiceClient

from .models import Cart, CartItem
from .serializers import CartItemCreateSerializer, CartItemSerializer, CartItemUpdateSerializer, CartSerializer


def api_response(*, data=None, message="Success", success=True, status_code=200):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def get_or_create_cart(customer):
    cart, _ = Cart.objects.get_or_create(customer=customer)
    return cart


def fetch_product(product_type, product_id):
    if product_type == CartItem.ProductTypes.LAPTOP:
        return LaptopServiceClient().detail(product_id)
    return MobileServiceClient().detail(product_id)


class CartView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        return api_response(message="Cart is ready", data=CartSerializer(cart).data, status_code=status.HTTP_201_CREATED)

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return api_response(message="Cart fetched successfully", data=CartSerializer(cart).data)


class CartItemCreateView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_cart(request.user)

        try:
            product = fetch_product(serializer.validated_data["product_type"], serializer.validated_data["product_id"])
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        quantity = serializer.validated_data["quantity"]
        if int(product["stock"]) < quantity:
            return api_response(message="Product does not have enough stock.", success=False, status_code=status.HTTP_400_BAD_REQUEST)

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
                return api_response(message="Updated quantity exceeds current stock.", success=False, status_code=status.HTTP_400_BAD_REQUEST)
            item.save()

        return api_response(message="Item added to cart successfully", data=CartItemSerializer(item).data, status_code=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def put(self, request, item_id):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_cart(request.user)
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if not item:
            return api_response(message="Cart item not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

        try:
            product = fetch_product(item.product_type, item.product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        quantity = serializer.validated_data["quantity"]
        if int(product["stock"]) < quantity:
            return api_response(message="Requested quantity exceeds stock.", success=False, status_code=status.HTTP_400_BAD_REQUEST)

        item.quantity = quantity
        item.save()
        return api_response(message="Cart item updated successfully", data=CartItemSerializer(item).data)


    def delete(self, request, item_id):
        cart = get_or_create_cart(request.user)
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if not item:
            return api_response(message="Cart item not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)
        item.delete()
        return api_response(message="Cart item deleted successfully", data=None)


class CartSummaryView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return api_response(
            message="Cart summary fetched successfully",
            data={
                "cart_id": cart.id,
                "total_items": cart.items.count(),
                "total_quantity": sum(item.quantity for item in cart.items.all()),
                "total_amount": cart.total_amount,
                "items": CartItemSerializer(cart.items.all(), many=True).data,
            },
        )
