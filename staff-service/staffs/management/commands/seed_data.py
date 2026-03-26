from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


STAFF_ACCOUNTS = [
    {
        "username": "admin",
        "full_name": "System Admin",
        "email": "admin@digitalshop.local",
        "password": "admin123",
    },
    {
        "username": "staff01",
        "full_name": "Le Thi Thu",
        "email": "staff01@digitalshop.local",
        "password": "staff123",
    },
]


class Command(BaseCommand):
    help = "Seed default staff accounts"

    def handle(self, *args, **options):
        staff_model = get_user_model()
        for account in STAFF_ACCOUNTS:
            payload = account.copy()
            password = payload.pop("password")
            staff_model.objects.get_or_create(
                username=payload["username"],
                defaults={**payload, "role": "STAFF"},
            )
            user = staff_model.objects.get(username=payload["username"])
            user.full_name = payload["full_name"]
            user.email = payload["email"]
            user.role = "STAFF"
            user.set_password(password)
            user.save()

        self.stdout.write(self.style.SUCCESS("Default staff accounts created or updated successfully."))
