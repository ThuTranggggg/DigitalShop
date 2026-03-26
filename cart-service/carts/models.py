from decimal import Decimal

from django.db import models


class Cart(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CHECKED_OUT = "CHECKED_OUT", "Checked out"

    customer_id = models.PositiveIntegerField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Cart {self.pk} - Customer {self.customer_id}"

    @property
    def total_amount(self):
        total = self.items.aggregate(total=models.Sum("subtotal"))["total"]
        return total or Decimal("0.00")


class CartItem(models.Model):
    class ProductTypes(models.TextChoices):
        LAPTOP = "LAPTOP", "Laptop"
        CLOTHES = "CLOTHES", "Clothes"

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=20, choices=ProductTypes.choices)
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("cart", "product_type", "product_id")
        ordering = ["id"]

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.unit_price) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product_name} x {self.quantity}"
