from django.core.management.base import BaseCommand

from laptops.models import LaptopProduct


LAPTOPS = [
    {
        "name": "Dell XPS 13",
        "brand": "Dell",
        "cpu": "Intel Core Ultra 7",
        "ram": "16GB",
        "storage": "512GB SSD",
        "screen": "13.4 inch FHD+",
        "price": "32990000",
        "stock": 8,
        "description": "Ultrabook cao cap cho cong viec va di chuyen.",
        "image_url": "https://via.placeholder.com/300x200?text=Dell+XPS+13",
    },
    {
        "name": "MacBook Air M3",
        "brand": "Apple",
        "cpu": "Apple M3",
        "ram": "16GB",
        "storage": "512GB SSD",
        "screen": "13.6 inch Liquid Retina",
        "price": "35990000",
        "stock": 6,
        "description": "Mau laptop mong nhe, thoi luong pin tot.",
        "image_url": "https://via.placeholder.com/300x200?text=MacBook+Air+M3",
    },
    {
        "name": "Lenovo ThinkPad X1 Carbon",
        "brand": "Lenovo",
        "cpu": "Intel Core i7",
        "ram": "16GB",
        "storage": "1TB SSD",
        "screen": "14 inch 2.8K OLED",
        "price": "38990000",
        "stock": 5,
        "description": "Do ben cao, phu hop doanh nghiep.",
        "image_url": "https://via.placeholder.com/300x200?text=ThinkPad+X1",
    },
    {
        "name": "ASUS ROG Zephyrus G14",
        "brand": "ASUS",
        "cpu": "AMD Ryzen 9",
        "ram": "32GB",
        "storage": "1TB SSD",
        "screen": "14 inch QHD 165Hz",
        "price": "42990000",
        "stock": 4,
        "description": "Laptop gaming hieu nang cao.",
        "image_url": "https://via.placeholder.com/300x200?text=ASUS+ROG+G14",
    },
    {
        "name": "HP Pavilion 15",
        "brand": "HP",
        "cpu": "Intel Core i5",
        "ram": "8GB",
        "storage": "512GB SSD",
        "screen": "15.6 inch FHD",
        "price": "18990000",
        "stock": 10,
        "description": "Laptop tam trung cho hoc tap va van phong.",
        "image_url": "https://via.placeholder.com/300x200?text=HP+Pavilion+15",
    },
    {
        "name": "MacBook Pro 14",
        "brand": "Apple",
        "cpu": "Apple M3 Pro",
        "ram": "18GB",
        "storage": "512GB SSD",
        "screen": "14.2 inch Liquid Retina XDR",
        "price": "58990000",
        "stock": 5,
        "description": "Laptop pro cho cac nha phat trien va thiet ke.",
        "image_url": "https://via.placeholder.com/300x200?text=MacBook+Pro+14",
    },
]


class Command(BaseCommand):
    help = "Seed sample laptops"

    def handle(self, *args, **options):
        created = 0
        for payload in LAPTOPS:
            _, was_created = LaptopProduct.objects.get_or_create(
                name=payload["name"],
                defaults=payload,
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seeded laptops. Created: {created}"))
