from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InventoryImportHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_type", models.CharField(choices=[("LAPTOP", "Laptop"), ("CLOTHES", "Clothes")], max_length=20)),
                ("product_id", models.PositiveIntegerField()),
                ("product_name", models.CharField(max_length=255)),
                ("quantity_added", models.PositiveIntegerField()),
                ("stock_before", models.PositiveIntegerField()),
                ("stock_after", models.PositiveIntegerField()),
                ("note", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("staff", models.ForeignKey(on_delete=models.CASCADE, related_name="inventory_imports", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
