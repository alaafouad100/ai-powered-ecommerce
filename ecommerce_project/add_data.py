import os
import sys
from pathlib import Path
import django

# ضبط مسار المشروع الأساسي
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product

def populate():
    # 1. إنشاء الفئات (باستخدام name فقط)
    cat_laptops, _ = Category.objects.get_or_create(name='Laptops')
    cat_phones, _ = Category.objects.get_or_create(name='Smartphones')
    cat_audio, _ = Category.objects.get_or_create(name='Audio')
    cat_accessories, _ = Category.objects.get_or_create(name='Accessories')

    # 2. قائمة المنتجات المتنوعة
    products_data = [
        # Laptops
        {"name": "MacBook Pro 16 M3", "cat": cat_laptops, "price": 2499.00, "desc": "Apple M3 Pro chip, 18GB RAM, 512GB SSD, Liquid Retina XDR display for heavy creative work."},
        {"name": "Lenovo Legion Pro 5", "cat": cat_laptops, "price": 1450.00, "desc": "High performance gaming laptop with AMD Ryzen 7, RTX 4060 graphics, and 16GB RAM."},
        {"name": "ASUS ROG Zephyrus G14", "cat": cat_laptops, "price": 1699.00, "desc": "Compact ultraportable gaming laptop with OLED 120Hz display and powerful RTX graphics."},
        {"name": "Dell Inspiron 15", "cat": cat_laptops, "price": 650.00, "desc": "Budget-friendly everyday laptop with Intel Core i5, 8GB RAM, and 512GB SSD storage."},
        
        # Smartphones
        {"name": "iPhone 15 Pro Max", "cat": cat_phones, "price": 1199.00, "desc": "Titanium design, A17 Pro chip, 48MP main camera with 5x telephoto optical zoom."},
        {"name": "Samsung Galaxy S24 Ultra", "cat": cat_phones, "price": 1299.00, "desc": "Built-in S-Pen, AI camera enhancement, Snapdragon 8 Gen 3, and stunning Dynamic AMOLED display."},
        {"name": "Google Pixel 8 Pro", "cat": cat_phones, "price": 899.00, "desc": "Google Tensor G3 chip, best-in-class computational photography, and clean Android experience."},
        {"name": "Xiaomi 14 Ultra", "cat": cat_phones, "price": 950.00, "desc": "Leica quad optical camera system, fast charging, and premium flagship display."},

        # Audio
        {"name": "Sony WH-1000XM5", "cat": cat_audio, "price": 399.00, "desc": "Industry leading noise canceling wireless headphones with crystal clear hands-free calling."},
        {"name": "Apple AirPods Pro 2", "cat": cat_audio, "price": 249.00, "desc": "Active Noise Cancellation, Adaptive Audio, and USB-C MagSafe charging case."},
        {"name": "Bose QuietComfort 45", "cat": cat_audio, "price": 329.00, "desc": "Legendary noise cancellation, lightweight comfort, and rich deep audio performance."},

        # Accessories
        {"name": "Logitech MX Master 3S", "cat": cat_accessories, "price": 99.00, "desc": "Ergonomic wireless performance mouse with quiet clicks and 8K DPI any-surface tracking."},
        {"name": "Keychron K2 Mechanical Keyboard", "cat": cat_accessories, "price": 85.00, "desc": "Wireless mechanical keyboard with RGB backlighting, hot-swappable switches for Mac and Windows."},
        {"name": "Anker 737 Power Bank", "cat": cat_accessories, "price": 120.00, "desc": "24,000mAh external battery with 140W ultra-fast charging and smart digital display."}
    ]

    count = 0
    for item in products_data:
        obj, created = Product.objects.get_or_create(
            name=item["name"],
            category=item["cat"],
            defaults={
                "description": item["desc"],
                "price": item["price"],
                "stock": 15
            }
        )
        if created:
            count += 1

    print(f"Done! Added {count} new products to database.")

if __name__ == '__main__':
    populate()