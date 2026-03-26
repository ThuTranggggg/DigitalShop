from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from customers.models import Invoice, InvoiceItem


CUSTOMERS = [
    {
        "username": "customer01",
        "full_name": "Nguyen Van A",
        "email": "customer01@digitalshop.local",
        "phone": "0900000001",
        "password": "customer123",
    },
    {
        "username": "customer02",
        "full_name": "Tran Thi B",
        "email": "customer02@digitalshop.local",
        "phone": "0900000002",
        "password": "customer123",
    },
]


def seed_demo_invoices(customer):
    pending_invoice, _ = Invoice.objects.get_or_create(
        invoice_code="INV-DEMO-001",
        defaults={
            "customer": customer,
            "status": Invoice.Status.PENDING,
            "note": "Hoa don demo dang cho thanh toan",
            "total_amount": "33790000.00",
        },
    )
    if pending_invoice.items.count() == 0:
        InvoiceItem.objects.create(
            invoice=pending_invoice,
            product_type=InvoiceItem.ProductTypes.LAPTOP,
            product_id=1,
            product_name="Dell XPS 13",
            unit_price="32990000.00",
            quantity=1,
        )
        InvoiceItem.objects.create(
            invoice=pending_invoice,
            product_type=InvoiceItem.ProductTypes.CLOTHES,
            product_id=1,
            product_name="Ao so mi Oxford slim fit",
            unit_price="800000.00",
            quantity=1,
        )

    cancelled_invoice, _ = Invoice.objects.get_or_create(
        invoice_code="INV-DEMO-002",
        defaults={
            "customer": customer,
            "status": Invoice.Status.CANCELLED,
            "note": "Hoa don demo da huy",
            "total_amount": "1290000.00",
        },
    )
    if cancelled_invoice.items.count() == 0:
        InvoiceItem.objects.create(
            invoice=cancelled_invoice,
            product_type=InvoiceItem.ProductTypes.CLOTHES,
            product_id=3,
            product_name="Quan jeans straight wash",
            unit_price="1290000.00",
            quantity=1,
        )


class Command(BaseCommand):
    help = "Seed sample customers and invoices"

    def handle(self, *args, **options):
        customer_model = get_user_model()
        created_customers = []

        for entry in CUSTOMERS:
            payload = entry.copy()
            password = payload.pop("password")
            customer_model.objects.get_or_create(
                username=payload["username"],
                defaults={**payload, "role": "CUSTOMER"},
            )
            user = customer_model.objects.get(username=payload["username"])
            user.full_name = payload["full_name"]
            user.email = payload["email"]
            user.phone = payload["phone"]
            user.role = "CUSTOMER"
            user.set_password(password)
            user.save()
            created_customers.append(user)

        if created_customers:
            seed_demo_invoices(created_customers[0])

        self.stdout.write(self.style.SUCCESS("Sample customers and invoices seeded successfully."))
