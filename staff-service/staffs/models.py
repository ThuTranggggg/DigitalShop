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


class InventoryImportHistory(models.Model):
    class ProductTypes(models.TextChoices):
        LAPTOP = "LAPTOP", "Laptop"
        CLOTHES = "CLOTHES", "Clothes"

    staff = models.ForeignKey(StaffUser, on_delete=models.CASCADE, related_name="inventory_imports")
    product_type = models.CharField(max_length=20, choices=ProductTypes.choices)
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255)
    quantity_added = models.PositiveIntegerField()
    stock_before = models.PositiveIntegerField()
    stock_after = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.product_name} +{self.quantity_added}"
