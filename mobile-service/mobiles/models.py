from django.db import models


class Mobile(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=120)
    chip = models.CharField(max_length=120)
    ram = models.CharField(max_length=64)
    storage = models.CharField(max_length=64)
    battery = models.CharField(max_length=64)
    camera = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.brand})"
