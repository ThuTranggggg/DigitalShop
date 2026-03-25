from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomerUser


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
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if user.role != CustomerUser.Roles.CUSTOMER:
            raise serializers.ValidationError("This account is not allowed to access customer-service.")
        attrs["user"] = user
        return attrs
