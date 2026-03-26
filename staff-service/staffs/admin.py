from django.contrib import admin

from .models import InventoryImportHistory, StaffUser


@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "email", "role", "created_at")
    search_fields = ("username", "full_name", "email")


@admin.register(InventoryImportHistory)
class InventoryImportHistoryAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_type", "quantity_added", "stock_before", "stock_after", "created_at")
    list_filter = ("product_type", "created_at")
    search_fields = ("product_name", "note")
