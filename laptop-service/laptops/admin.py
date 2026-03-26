from django.contrib import admin

from .models import LaptopProduct


@admin.register(LaptopProduct)
class LaptopProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "price", "stock", "status", "updated_at")
    list_filter = ("brand", "status")
    search_fields = ("name", "brand", "cpu")
