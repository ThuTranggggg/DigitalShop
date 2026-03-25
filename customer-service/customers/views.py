from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsCustomerUser
from .serializers import CustomerLoginSerializer, CustomerProfileSerializer, CustomerRegisterSerializer
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


class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return api_response(message="Customer registered successfully", data=CustomerProfileSerializer(user).data, status_code=status.HTTP_201_CREATED)


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


class CustomerMobileListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = MobileServiceClient().list(params=request.query_params)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Mobile list fetched successfully", data=data)


class CustomerMobileSearchView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        try:
            data = MobileServiceClient().search(params=request.query_params)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Mobile search completed successfully", data=data)


class CustomerMobileDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request, product_id):
        try:
            data = MobileServiceClient().detail(product_id)
        except ServiceClientError as exc:
            return api_response(message=str(exc), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        return api_response(message="Mobile detail fetched successfully", data=data)
