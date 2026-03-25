from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_type",
            "product_id",
            "product_name",
            "unit_price",
            "quantity",
            "subtotal",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "customer", "created_at", "updated_at", "items", "total_amount"]


class CartItemCreateSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(choices=CartItem.ProductTypes.choices)
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
