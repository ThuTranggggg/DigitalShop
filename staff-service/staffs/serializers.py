from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import InventoryImportHistory, StaffUser


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = [
            "id",
            "full_name",
            "username",
            "email",
            "role",
            "created_at",
            "updated_at",
        ]


class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if user.role != StaffUser.Roles.STAFF:
            raise serializers.ValidationError("This account is not allowed to access staff-service.")
        attrs["user"] = user
        return attrs


class LaptopPayloadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    brand = serializers.CharField(max_length=120)
    cpu = serializers.CharField(max_length=120)
    ram = serializers.CharField(max_length=64)
    storage = serializers.CharField(max_length=64)
    screen = serializers.CharField(max_length=120)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    stock = serializers.IntegerField(min_value=0)
    description = serializers.CharField(required=False, allow_blank=True)
    image_url = serializers.URLField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=[("ACTIVE", "Active"), ("HIDDEN", "Hidden")], required=False)


class ClothesPayloadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    brand = serializers.CharField(max_length=120)
    category = serializers.CharField(max_length=80)
    size = serializers.CharField(max_length=32)
    material = serializers.CharField(max_length=120)
    color = serializers.CharField(max_length=64)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    stock = serializers.IntegerField(min_value=0)
    description = serializers.CharField(required=False, allow_blank=True)
    image_url = serializers.URLField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=[("ACTIVE", "Active"), ("HIDDEN", "Hidden")], required=False)


class InventoryImportSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(choices=InventoryImportHistory.ProductTypes.choices)
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(required=False, allow_blank=True, max_length=255)


class InventoryImportHistorySerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source="staff.full_name", read_only=True)

    class Meta:
        model = InventoryImportHistory
        fields = [
            "id",
            "staff",
            "staff_name",
            "product_type",
            "product_id",
            "product_name",
            "quantity_added",
            "stock_before",
            "stock_after",
            "note",
            "created_at",
        ]
