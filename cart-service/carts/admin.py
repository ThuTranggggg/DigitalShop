from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "status", "updated_at")
    list_filter = ("status", "updated_at")
    search_fields = ("customer_id",)
    inlines = [CartItemInline]
