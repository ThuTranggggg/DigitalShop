from rest_framework import serializers

from .models import Laptop


class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
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
            "created_at",
            "updated_at",
        ]
