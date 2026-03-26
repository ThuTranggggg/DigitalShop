from django.db.models import F, Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LaptopProduct
from .serializers import LaptopProductSerializer, StockAdjustmentSerializer


def api_response(*, data=None, message="Success", success=True, status_code=200):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


class LaptopQuerySetMixin:
    queryset = LaptopProduct.objects.all()
    serializer_class = LaptopProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.query_params.get("brand")
        keyword = self.request.query_params.get("q")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        status_filter = self.request.query_params.get("status")

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(brand__icontains=keyword)
                | Q(cpu__icontains=keyword)
            )
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class LaptopListCreateView(LaptopQuerySetMixin, generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data, message="Laptops fetched successfully")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            data=serializer.data,
            message="Laptop created successfully",
            status_code=status.HTTP_201_CREATED,
        )


class LaptopDetailView(LaptopQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_response(data=serializer.data, message="Laptop fetched successfully")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(data=serializer.data, message="Laptop updated successfully")

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return api_response(data=None, message="Laptop deleted successfully")


class LaptopSearchView(LaptopListCreateView):
    pass


class LaptopStockAdjustView(APIView):
    def post(self, request, pk):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = LaptopProduct.objects.filter(pk=pk).first()
        if not product:
            return api_response(
                success=False,
                message="Laptop product not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        quantity_delta = serializer.validated_data["quantity_delta"]
        if product.stock + quantity_delta < 0:
            return api_response(
                success=False,
                message="Stock adjustment would make inventory negative.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        product.stock = F("stock") + quantity_delta
        product.save(update_fields=["stock"])
        product.refresh_from_db()
        return api_response(data=LaptopProductSerializer(product).data, message="Laptop stock updated successfully")
