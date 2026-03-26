from decimal import Decimal

from django.conf import settings
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


class Invoice(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices")
    invoice_code = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    note = models.CharField(max_length=255, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.invoice_code


class InvoiceItem(models.Model):
    class ProductTypes(models.TextChoices):
        LAPTOP = "LAPTOP", "Laptop"
        CLOTHES = "CLOTHES", "Clothes"

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=20, choices=ProductTypes.choices)
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.unit_price) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product_name} x {self.quantity}"
