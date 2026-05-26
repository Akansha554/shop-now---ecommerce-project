import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product

products = [
    {"title": "Wireless Headphones", "price": 150.0, "description": "High-quality wireless headphones with noise cancellation.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "sold": False, "is_sale": True},
    {"title": "Gaming Laptop", "price": 1200.0, "description": "High-performance laptop for gaming and productivity.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400", "sold": False, "is_sale": False},
    {"title": "Running Shoes", "price": 85.0, "description": "Lightweight running shoes for everyday training.", "category": "Sports", "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "sold": False, "is_sale": True},
    {"title": "Coffee Maker", "price": 60.0, "description": "Automatic drip coffee maker with 12-cup capacity.", "category": "Kitchen", "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400", "sold": False, "is_sale": False},
    {"title": "Yoga Mat", "price": 35.0, "description": "Non-slip yoga mat with carrying strap.", "category": "Sports", "image_url": "https://images.unsplash.com/photo-1601925228008-4bb42b1e0a3b?w=400", "sold": False, "is_sale": False},
    {"title": "Smartwatch", "price": 250.0, "description": "Feature-packed smartwatch with health tracking.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", "sold": False, "is_sale": True},
    {"title": "Backpack", "price": 70.0, "description": "Durable 30L backpack for travel and hiking.", "category": "Travel", "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "sold": False, "is_sale": False},
    {"title": "Desk Lamp", "price": 45.0, "description": "LED desk lamp with adjustable brightness.", "category": "Home", "image_url": "https://images.unsplash.com/photo-1543198126-a8ad8e47fb22?w=400", "sold": False, "is_sale": False},
    {"title": "Bluetooth Speaker", "price": 90.0, "description": "Portable waterproof Bluetooth speaker.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "sold": False, "is_sale": True},
    {"title": "Cookware Set", "price": 120.0, "description": "10-piece non-stick cookware set.", "category": "Kitchen", "image_url": "https://images.unsplash.com/photo-1584990347449-39e171f89765?w=400", "sold": False, "is_sale": False},
    {"title": "Sunglasses", "price": 55.0, "description": "UV400 polarized sunglasses.", "category": "Fashion", "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400", "sold": False, "is_sale": True},
    {"title": "Mechanical Keyboard", "price": 110.0, "description": "Tactile mechanical keyboard with RGB backlighting.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400", "sold": False, "is_sale": False},
]

Product.objects.all().delete()
for p in products:
    Product.objects.create(**p)

print(f"✅ Seeded {len(products)} products successfully.")