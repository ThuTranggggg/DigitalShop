from django.contrib import admin

from .models import ClothesProduct


@admin.register(ClothesProduct)
class ClothesProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "size", "price", "stock", "status")
    list_filter = ("brand", "category", "status")
    search_fields = ("name", "brand", "category", "material")
