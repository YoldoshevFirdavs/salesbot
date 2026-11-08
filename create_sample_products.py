import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tgbot.models import Category, Product
from decimal import Decimal

# Sample products data with multilingual names and descriptions
products_data = [
    # Hamburgers
    {
        'category_name': 'Cheeseburger',
        'name_uz': 'Klassik Cheeseburger',
        'name_ru': 'Классический Чизбургер',
        'name_eng': 'Classic Cheeseburger',
        'description_uz': 'Go\'sht, pishloq, pomidor, salat',
        'description_ru': 'Мясо, сыр, помидор, салат',
        'description_eng': 'Beef, cheese, tomato, lettuce',
        'price': Decimal('25000'),
        'stock': 50
    },
    {
        'category_name': 'Cheeseburger',
        'name_uz': 'Double Cheeseburger',
        'name_ru': 'Двойной Чизбургер',
        'name_eng': 'Double Cheeseburger',
        'description_uz': 'Ikki qavat go\'sht, pishloq, pomidor',
        'description_ru': 'Два слоя мяса, сыр, помидор',
        'description_eng': 'Two beef patties, cheese, tomato',
        'price': Decimal('35000'),
        'stock': 40
    },
    {
        'category_name': 'Chicken Burger',
        'name_uz': 'Tovuqli Burger',
        'name_ru': 'Куриный Бургер',
        'name_eng': 'Chicken Burger',
        'description_uz': 'Tovuq go\'shti, sous, salat',
        'description_ru': 'Куриное мясо, соус, салат',
        'description_eng': 'Chicken patty, sauce, lettuce',
        'price': Decimal('22000'),
        'stock': 45
    },
    {
        'category_name': 'Bacon Cheeseburger',
        'name_uz': 'Bekonli Cheeseburger',
        'name_ru': 'Чизбургер с Беконом',
        'name_eng': 'Bacon Cheeseburger',
        'description_uz': 'Go\'sht, bekon, pishloq, sous',
        'description_ru': 'Мясо, бекон, сыр, соус',
        'description_eng': 'Beef, bacon, cheese, sauce',
        'price': Decimal('30000'),
        'stock': 35
    },
    # Pizzas
    {
        'category_name': 'BBQ Chicken',
        'name_uz': 'BBQ Tovuqli Pitsa',
        'name_ru': 'Пицца с Курицей BBQ',
        'name_eng': 'BBQ Chicken Pizza',
        'description_uz': 'Tovuq, BBQ sous, piyoz, pomidor',
        'description_ru': 'Курица, соус BBQ, лук, помидор',
        'description_eng': 'Chicken, BBQ sauce, onion, tomato',
        'price': Decimal('45000'),
        'stock': 30
    },
    {
        'category_name': 'BBQ Chicken',
        'name_uz': 'Katta BBQ Pitsa',
        'name_ru': 'Большая BBQ Пицца',
        'name_eng': 'Large BBQ Pizza',
        'description_uz': 'Katta o\'lcham, tovuq, BBQ sous',
        'description_ru': 'Большой размер, курица, соус BBQ',
        'description_eng': 'Large size, chicken, BBQ sauce',
        'price': Decimal('60000'),
        'stock': 25
    },
    # Chicken Products
    {
        'category_name': 'Chicken Nuggets',
        'name_uz': 'Tovuq Nuggetslari (6 dona)',
        'name_ru': 'Куриные Наггетсы (6 шт)',
        'name_eng': 'Chicken Nuggets (6 pcs)',
        'description_uz': '6 dona qovurilgan tovuq naggetslar',
        'description_ru': '6 хрустящих куриных наггетсов',
        'description_eng': '6 crispy chicken nuggets',
        'price': Decimal('18000'),
        'stock': 60
    },
    {
        'category_name': 'Chicken Nuggets',
        'name_uz': 'Tovuq Nuggetslari (12 dona)',
        'name_ru': 'Куриные Наггетсы (12 шт)',
        'name_eng': 'Chicken Nuggets (12 pcs)',
        'description_uz': '12 dona qovurilgan tovuq naggetslar',
        'description_ru': '12 хрустящих куриных наггетсов',
        'description_eng': '12 crispy chicken nuggets',
        'price': Decimal('32000'),
        'stock': 50
    },
]

print("🚀 Creating sample products...")

for data in products_data:
    try:
        # Find category by name
        category = Category.objects.filter(name_uz__icontains=data['category_name']).first()
        if not category:
            category = Category.objects.filter(name_eng__icontains=data['category_name']).first()
        
        if not category:
            print(f"❌ Category not found: {data['category_name']}")
            continue
        
        # Check if product already exists
        existing = Product.objects.filter(
            name_uz=data['name_uz'],
            category=category
        ).first()
        
        if existing:
            print(f"⏭️  Product already exists: {data['name_uz']}")
            continue
        
        # Create product
        product = Product.objects.create(
            name_uz=data['name_uz'],
            name_ru=data['name_ru'],
            name_eng=data['name_eng'],
            description_uz=data['description_uz'],
            description_ru=data['description_ru'],
            description_eng=data['description_eng'],
            price=data['price'],
            stock=data['stock'],
            category=category,
            is_active=True
        )
        
        print(f"✅ Created: {product.name_uz} (ID: {product.id}) in {category.name_uz}")
        
    except Exception as e:
        print(f"❌ Error creating {data.get('name_uz', 'unknown')}: {e}")

print(f"\n📊 Total products: {Product.objects.count()}")
print(f"📊 Active products: {Product.objects.filter(is_active=True).count()}")
