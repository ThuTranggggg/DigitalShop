from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsStaffUser
from .serializers import StaffLoginSerializer, StaffProfileSerializer
from .services.base_client import ServiceClientError
from .services.laptop_client import LaptopServiceClient
from .services.mobile_client import MobileServiceClient


def api_response(*, data=None, message="Success", success=True, status_code=200):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


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
        try:
            data = LaptopServiceClient().create_laptop(request.data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop created successfully", data=data, status_code=status.HTTP_201_CREATED)


class StaffLaptopDetailView(APIView):
    permission_classes = [IsStaffUser]

    def put(self, request, product_id):
        try:
            data = LaptopServiceClient().update_laptop(product_id, request.data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop updated successfully", data=data)


    def delete(self, request, product_id):
        try:
            LaptopServiceClient().delete_laptop(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Laptop deleted successfully", data=None)


class StaffMobileCreateView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        try:
            data = MobileServiceClient().create_mobile(request.data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Mobile created successfully", data=data, status_code=status.HTTP_201_CREATED)


class StaffMobileDetailView(APIView):
    permission_classes = [IsStaffUser]

    def put(self, request, product_id):
        try:
            data = MobileServiceClient().update_mobile(product_id, request.data)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Mobile updated successfully", data=data)


    def delete(self, request, product_id):
        try:
            MobileServiceClient().delete_mobile(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Mobile deleted successfully", data=None)


class StaffProductsOverviewView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        try:
            laptops = LaptopServiceClient().list_laptops()
            mobiles = MobileServiceClient().list_mobiles()
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(
            message="Products overview fetched successfully",
            data={
                "total_laptops": len(laptops),
                "total_mobiles": len(mobiles),
                "laptops": laptops,
                "mobiles": mobiles,
            },
        )
