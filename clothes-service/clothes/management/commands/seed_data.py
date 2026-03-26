from django.core.management.base import BaseCommand

from clothes.models import ClothesProduct


CLOTHES_PRODUCTS = [
    {
        "name": "Ao so mi Oxford slim fit",
        "brand": "Routine",
        "category": "Shirt",
        "size": "M",
        "material": "Cotton Oxford",
        "color": "White",
        "price": "590000",
        "stock": 40,
        "description": "Ao so mi cong so form gon, de demo khu thoi trang.",
        "image_url": "https://via.placeholder.com/300x200?text=Oxford+Shirt",
    },
    {
        "name": "Ao polo basic premium",
        "brand": "Coolmate",
        "category": "Polo",
        "size": "L",
        "material": "Pique Cotton",
        "color": "Navy",
        "price": "390000",
        "stock": 55,
        "description": "Ao polo toi gian, de ban va de chup man hinh demo.",
        "image_url": "https://via.placeholder.com/300x200?text=Polo+Premium",
    },
    {
        "name": "Quan jeans straight wash",
        "brand": "Levi's",
        "category": "Jeans",
        "size": "32",
        "material": "Denim",
        "color": "Indigo",
        "price": "1290000",
        "stock": 24,
        "description": "Quan jeans phom dung, de phoi do hang ngay.",
        "image_url": "https://via.placeholder.com/300x200?text=Straight+Jeans",
    },
    {
        "name": "Ao hoodie fleece urban",
        "brand": "DirtyCoins",
        "category": "Hoodie",
        "size": "XL",
        "material": "Fleece",
        "color": "Black",
        "price": "890000",
        "stock": 18,
        "description": "Hoodie chat lieu day, phu hop mua lanh.",
        "image_url": "https://via.placeholder.com/300x200?text=Urban+Hoodie",
    },
    {
        "name": "Vay midi thanh lich",
        "brand": "IVY Moda",
        "category": "Dress",
        "size": "S",
        "material": "Poly blend",
        "color": "Beige",
        "price": "990000",
        "stock": 21,
        "description": "Vay midi thanh lich, hop demo cho nhom san pham nu.",
        "image_url": "https://via.placeholder.com/300x200?text=Midi+Dress",
    },
    {
        "name": "Ao khoac bomber daily",
        "brand": "5TheWay",
        "category": "Jacket",
        "size": "L",
        "material": "Polyester",
        "color": "Olive",
        "price": "1150000",
        "stock": 16,
        "description": "Ao khoac bomber gon gang, tre trung.",
        "image_url": "https://via.placeholder.com/300x200?text=Bomber+Jacket",
    },
    {
        "name": "Quan short kaki summer",
        "brand": "Uniqlo",
        "category": "Shorts",
        "size": "M",
        "material": "Kaki Stretch",
        "color": "Khaki",
        "price": "490000",
        "stock": 34,
        "description": "Quan short mac hang ngay, de ban trong mua nong.",
        "image_url": "https://via.placeholder.com/300x200?text=Kaki+Shorts",
    },
    {
        "name": "Ao len cardigan soft touch",
        "brand": "Hnoss",
        "category": "Cardigan",
        "size": "Free Size",
        "material": "Acrylic blend",
        "color": "Cream",
        "price": "760000",
        "stock": 19,
        "description": "Cardigan mem, phu hop bo suu tap thu dong.",
        "image_url": "https://via.placeholder.com/300x200?text=Soft+Cardigan",
    },
]


class Command(BaseCommand):
    help = "Seed sample clothes products"

    def handle(self, *args, **options):
        created = 0
        for payload in CLOTHES_PRODUCTS:
            _, was_created = ClothesProduct.objects.get_or_create(
                name=payload["name"],
                defaults=payload,
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seeded clothes products. Created: {created}"))
