from rest_framework import serializers

from .models import LaptopProduct


class LaptopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaptopProduct
        fields = [
            "id",
            "name",
            "brand",
            "cpu",
            "ram",
            "storage",
            "screen",
            "price",
            "stock",
            "description",
            "image_url",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class StockAdjustmentSerializer(serializers.Serializer):
    quantity_delta = serializers.IntegerField()
    note = serializers.CharField(required=False, allow_blank=True)
