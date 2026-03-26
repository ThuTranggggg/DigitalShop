import uuid
from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from carts.services.cart_client import CartServiceClient

from .models import Invoice, InvoiceItem
from .permissions import IsCustomerUser
from .serializers import (
    CheckoutSerializer,
    CustomerLoginSerializer,
    CustomerProfileSerializer,
    CustomerRegisterSerializer,
    InvoiceSerializer,
)
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


def get_product_client(product_type):
    if product_type == InvoiceItem.ProductTypes.LAPTOP:
        return LaptopServiceClient()
    return ClothesServiceClient()


class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return api_response(
            message="Customer registered successfully",
            data=CustomerProfileSerializer(user).data,
            status_code=status.HTTP_201_CREATED,
        )


class CustomerLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return api_response(
            message="Customer login successful",
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "customer": CustomerProfileSerializer(user).data,
            },
        )


class CustomerProfileView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        return api_response(message="Customer profile fetched successfully", data=CustomerProfileSerializer(request.user).data)


class CustomerLaptopListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = LaptopServiceClient().list(params=request.query_params)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop list fetched successfully", data=data)


class CustomerLaptopSearchView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = LaptopServiceClient().search(params=request.query_params)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop search completed successfully", data=data)


class CustomerLaptopDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request, product_id):
        try:
            data = LaptopServiceClient().detail(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop detail fetched successfully", data=data)


class CustomerClothesListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = ClothesServiceClient().list(params=request.query_params)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Clothes list fetched successfully", data=data)


class CustomerClothesSearchView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = ClothesServiceClient().search(params=request.query_params)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Clothes search completed successfully", data=data)


class CustomerClothesDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request, product_id):
        try:
            data = ClothesServiceClient().detail(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Clothes detail fetched successfully", data=data)


class CheckoutView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart_summary = CartServiceClient().summary(request.user.id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        cart_items = cart_summary.get("items", [])
        if not cart_items:
            return api_response(
                message="Cart is empty. Please add products before checkout.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        validated_items = []
        for item in cart_items:
            try:
                product = get_product_client(item["product_type"]).detail(item["product_id"])
            except ServiceClientError as exc:
                return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

            if int(product["stock"]) < int(item["quantity"]):
                return api_response(
                    message=f"Product '{product['name']}' does not have enough stock for checkout.",
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            validated_items.append(
                {
                    "product_type": item["product_type"],
                    "product_id": item["product_id"],
                    "product_name": product["name"],
                    "unit_price": Decimal(str(product["price"])),
                    "quantity": int(item["quantity"]),
                }
            )

        invoice_code = f"INV-{uuid.uuid4().hex[:10].upper()}"
        stock_adjustments_done = []

        try:
            with transaction.atomic():
                invoice = Invoice.objects.create(
                    customer=request.user,
                    invoice_code=invoice_code,
                    status=Invoice.Status.PENDING,
                    note=serializer.validated_data.get("note", ""),
                )

                total_amount = Decimal("0.00")
                for item in validated_items:
                    invoice_item = InvoiceItem.objects.create(
                        invoice=invoice,
                        product_type=item["product_type"],
                        product_id=item["product_id"],
                        product_name=item["product_name"],
                        unit_price=item["unit_price"],
                        quantity=item["quantity"],
                    )
                    total_amount += invoice_item.subtotal

                    get_product_client(item["product_type"]).adjust_stock(
                        item["product_id"],
                        -item["quantity"],
                    )
                    stock_adjustments_done.append((item["product_type"], item["product_id"], item["quantity"]))

                invoice.total_amount = total_amount
                invoice.status = Invoice.Status.PAID
                invoice.save(update_fields=["total_amount", "status", "updated_at"])
        except ServiceClientError as exc:
            for product_type, product_id, quantity in reversed(stock_adjustments_done):
                try:
                    get_product_client(product_type).adjust_stock(product_id, quantity)
                except ServiceClientError:
                    pass
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        try:
            CartServiceClient().clear(request.user.id)
        except ServiceClientError:
            pass

        return api_response(
            message="Checkout completed successfully",
            data=InvoiceSerializer(invoice).data,
            status_code=status.HTTP_201_CREATED,
        )


class InvoiceListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        invoices = Invoice.objects.filter(customer=request.user).prefetch_related("items")
        return api_response(message="Invoices fetched successfully", data=InvoiceSerializer(invoices, many=True).data)


class InvoiceDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request, invoice_id):
        invoice = Invoice.objects.filter(customer=request.user, id=invoice_id).prefetch_related("items").first()
        if not invoice:
            return api_response(message="Invoice not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)
        return api_response(message="Invoice detail fetched successfully", data=InvoiceSerializer(invoice).data)


class InvoiceCancelView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request, invoice_id):
        invoice = Invoice.objects.filter(customer=request.user, id=invoice_id).prefetch_related("items").first()
        if not invoice:
            return api_response(message="Invoice not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)
        if invoice.status != Invoice.Status.PENDING:
            return api_response(
                message="Only pending invoices can be cancelled.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        invoice.status = Invoice.Status.CANCELLED
        invoice.save(update_fields=["status", "updated_at"])
        return api_response(message="Invoice cancelled successfully", data=InvoiceSerializer(invoice).data)
