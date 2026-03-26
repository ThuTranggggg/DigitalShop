from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomerUser, Invoice, InvoiceItem


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = [
            "id",
            "full_name",
            "username",
            "email",
            "phone",
            "role",
            "created_at",
            "updated_at",
        ]


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomerUser
        fields = ["full_name", "username", "email", "phone", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomerUser(**validated_data)
        user.role = CustomerUser.Roles.CUSTOMER
        user.set_password(password)
        user.save()
        return user


class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if user.role != CustomerUser.Roles.CUSTOMER:
            raise serializers.ValidationError("This account is not allowed to access customer-service.")
        attrs["user"] = user
        return attrs


class CheckoutSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True, max_length=255)


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            "id",
            "product_type",
            "product_id",
            "product_name",
            "unit_price",
            "quantity",
            "subtotal",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_code",
            "status",
            "note",
            "total_amount",
            "created_at",
            "updated_at",
            "items",
        ]
