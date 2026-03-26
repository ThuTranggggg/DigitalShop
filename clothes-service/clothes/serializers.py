from rest_framework import serializers

from .models import ClothesProduct


class ClothesProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesProduct
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "size",
            "material",
            "color",
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
