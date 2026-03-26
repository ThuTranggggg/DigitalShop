from rest_framework import serializers


class CartItemCreateSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(choices=[("LAPTOP", "Laptop"), ("CLOTHES", "Clothes")])
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
