import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tgbot.models import Product
from django.core.files import File

print("🖼️  Assigning images to products...")

# Get all products ordered by ID
products = Product.objects.all().order_by('id')

for product in products:
    # Image file path
    image_path = f'media/products/main/product_{product.id}.jpg'
    
    if os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                product.main_image.save(
                    f'product_{product.id}.jpg',
                    File(f),
                    save=True
                )
            print(f"✅ Assigned image to: {product.name_uz} (ID: {product.id})")
        except Exception as e:
            print(f"❌ Failed to assign image to {product.name_uz}: {e}")
    else:
        print(f"⚠️  Image not found for: {product.name_uz} (ID: {product.id})")

print(f"\n📊 Products with images: {Product.objects.exclude(main_image='').count()}")
print(f"📊 Products without images: {Product.objects.filter(main_image='').count()}")
