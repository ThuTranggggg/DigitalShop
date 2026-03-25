from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


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


class Command(BaseCommand):
    help = "Seed sample customers"

    def handle(self, *args, **options):
        customer_model = get_user_model()
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

        self.stdout.write(self.style.SUCCESS("Sample customers seeded successfully."))
