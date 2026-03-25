from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed default staff account"

    def handle(self, *args, **options):
        staff_model = get_user_model()
        _, created = staff_model.objects.get_or_create(
            username="admin",
            defaults={
                "full_name": "System Admin",
                "email": "admin@digitalshop.local",
                "role": "STAFF",
            },
        )
        user = staff_model.objects.get(username="admin")
        user.set_password("admin123")
        user.save()
        message = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Default staff account {message} successfully."))
