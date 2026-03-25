from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import StaffUser


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
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if user.role != StaffUser.Roles.STAFF:
            raise serializers.ValidationError("This account is not allowed to access staff-service.")
        attrs["user"] = user
        return attrs
