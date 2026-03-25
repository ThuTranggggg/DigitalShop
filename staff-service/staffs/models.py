from django.contrib.auth.models import AbstractUser
from django.db import models


class StaffUser(AbstractUser):
    class Roles(models.TextChoices):
        STAFF = "STAFF", "Staff"

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STAFF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email", "full_name"]

    def __str__(self) -> str:
        return self.username
