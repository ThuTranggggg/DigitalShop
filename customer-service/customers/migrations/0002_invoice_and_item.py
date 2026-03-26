from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("invoice_code", models.CharField(max_length=32, unique=True)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("PAID", "Paid"), ("CANCELLED", "Cancelled")], default="PENDING", max_length=20)),
                ("note", models.CharField(blank=True, max_length=255)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("customer", models.ForeignKey(on_delete=models.CASCADE, related_name="invoices", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="InvoiceItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_type", models.CharField(choices=[("LAPTOP", "Laptop"), ("CLOTHES", "Clothes")], max_length=20)),
                ("product_id", models.PositiveIntegerField()),
                ("product_name", models.CharField(max_length=255)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("invoice", models.ForeignKey(on_delete=models.CASCADE, related_name="items", to="customers.invoice")),
            ],
            options={"ordering": ["id"]},
        ),
    ]
