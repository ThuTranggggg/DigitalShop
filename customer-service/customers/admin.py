from django.contrib import admin

from .models import CustomerUser, Invoice, InvoiceItem


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "email", "phone", "created_at")
    search_fields = ("username", "full_name", "email", "phone")


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_code", "customer", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("invoice_code", "customer__username", "customer__full_name")
    inlines = [InvoiceItemInline]
