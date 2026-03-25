from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomerUser(AbstractUser):
    class Roles(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email", "full_name", "phone"]

    def __str__(self) -> str:
        return self.username
