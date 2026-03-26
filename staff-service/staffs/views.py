from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import InventoryImportHistory
from .permissions import IsStaffUser
from .serializers import (
    ClothesPayloadSerializer,
    InventoryImportHistorySerializer,
    InventoryImportSerializer,
    LaptopPayloadSerializer,
    StaffLoginSerializer,
    StaffProfileSerializer,
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
    if product_type == InventoryImportHistory.ProductTypes.LAPTOP:
        return LaptopServiceClient()
    return ClothesServiceClient()


class StaffLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return api_response(
            message="Staff login successful",
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "staff": StaffProfileSerializer(user).data,
            },
        )


class StaffProfileView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        return api_response(
            message="Staff profile fetched successfully",
            data=StaffProfileSerializer(request.user).data,
        )


class StaffLaptopCreateView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        serializer = LaptopPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = LaptopServiceClient().create_laptop(serializer.validated_data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop created successfully", data=data, status_code=status.HTTP_201_CREATED)


class StaffLaptopDetailView(APIView):
    permission_classes = [IsStaffUser]

    def put(self, request, product_id):
        serializer = LaptopPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = LaptopServiceClient().update_laptop(product_id, serializer.validated_data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop updated successfully", data=data)

    def delete(self, request, product_id):
        try:
            LaptopServiceClient().delete_laptop(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop deleted successfully", data=None)


class StaffClothesCreateView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        serializer = ClothesPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = ClothesServiceClient().create_clothes(serializer.validated_data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Clothes product created successfully", data=data, status_code=status.HTTP_201_CREATED)


class StaffClothesDetailView(APIView):
    permission_classes = [IsStaffUser]

    def put(self, request, product_id):
        serializer = ClothesPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = ClothesServiceClient().update_clothes(product_id, serializer.validated_data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Clothes product updated successfully", data=data)

    def delete(self, request, product_id):
        try:
            ClothesServiceClient().delete_clothes(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Clothes product deleted successfully", data=None)


class StaffInventoryImportView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        imports = InventoryImportHistory.objects.select_related("staff")[:20]
        return api_response(
            message="Inventory imports fetched successfully",
            data=InventoryImportHistorySerializer(imports, many=True).data,
        )

    def post(self, request):
        serializer = InventoryImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_type = serializer.validated_data["product_type"]
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        note = serializer.validated_data.get("note", "")

        client = get_product_client(product_type)

        try:
            product = client.detail(product_id)
            updated_product = client.adjust_stock(product_id, quantity)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        history = InventoryImportHistory.objects.create(
            staff=request.user,
            product_type=product_type,
            product_id=product_id,
            product_name=product["name"],
            quantity_added=quantity,
            stock_before=product["stock"],
            stock_after=updated_product["stock"],
            note=note,
        )

        return api_response(
            message="Inventory imported successfully",
            data={
                "import_history": InventoryImportHistorySerializer(history).data,
                "product": updated_product,
            },
            status_code=status.HTTP_201_CREATED,
        )


class StaffDashboardView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        try:
            laptops = LaptopServiceClient().list_laptops()
            clothes = ClothesServiceClient().list_clothes()
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)

        recent_imports = InventoryImportHistory.objects.select_related("staff")[:5]
        total_stock = sum(int(item.get("stock", 0)) for item in laptops) + sum(int(item.get("stock", 0)) for item in clothes)

        dashboard_data = {
            "total_products": len(laptops) + len(clothes),
            "total_stock": total_stock,
            "total_laptops": len(laptops),
            "total_clothes": len(clothes),
            "recent_import_count": InventoryImportHistory.objects.count(),
            "recent_imports": InventoryImportHistorySerializer(recent_imports, many=True).data,
            "laptops": laptops,
            "clothes": clothes,
        }
        return api_response(message="Staff dashboard fetched successfully", data=dashboard_data)


class StaffProductsOverviewView(StaffDashboardView):
    pass
