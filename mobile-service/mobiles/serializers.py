from rest_framework import serializers

from .models import Mobile


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = [
            "id",
            "name",
            "brand",
            "chip",
            "ram",
            "storage",
            "battery",
            "camera",
            "price",
            "stock",
            "description",
            "image_url",
            "created_at",
            "updated_at",
        ]
