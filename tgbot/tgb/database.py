import os
from decimal import Decimal

import psycopg2
from django.db import transaction
from tgbot.models import Category, Product, Order, OrderStatus
from users.models import CustomUser
from tgbot.tgb.logger import logger

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "salestgbot"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "root"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_user(self, telegram_id, chat_id):
        CustomUser.objects.create(
        telegram_id=telegram_id,
        chat_id=chat_id,
        state=1
        )

    def update_user_data(self, chat_id, key, value):
        CustomUser.objects.filter(chat_id=chat_id).update(**{key: value})

    def get_user_by_chat_id(self, chat_id):
        user = CustomUser.objects.filter(chat_id=chat_id).first()
        if user:
            return {
                'id': user.id,
                'chat_id': user.chat_id,
                'language': user.language,
                'state': user.state,
                'full_name': user.full_name,
                'phone_number': user.phone_number
            }
        return None

    def get_categories_by_parent(self, parent_id=None):
        if parent_id:
            categories = Category.objects.filter(parent_id=parent_id)
        else:
            categories = Category.objects.filter(parent_id__isnull=True)
        
        result = []
        for cat in categories:
            cat_data = {
                'id': cat.id,
                'name': cat.name_uz,
                'name_uz': cat.name_uz,
                'name_ru': cat.name_ru,
                'name_eng': cat.name_eng,
                'slug': cat.slug,
                'parent_id': cat.parent.id if cat.parent else None
            }
            result.append(cat_data)
        return result

    def get_category_parent(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
            if category.parent:
                return {
                    'id': category.parent.id,
                    'name': category.parent.name_uz,
                    'name_uz': category.parent.name_uz,
                    'name_ru': category.parent.name_ru,
                    'name_eng': category.parent.name_eng,
                    'parent_id': category.parent.parent.id if category.parent.parent else None
                }
            return None
        except Category.DoesNotExist:
            return None
    def get_products_by_category(self, category_id):
        """
        Berilgan kategoriya ID bo'yicha mavjud mahsulotlarni qaytaradi.
        """
        products = Product.available.filter(category_id=category_id)
        
        result = []
        for prod in products:
            prod_data = {
                'id': prod.id,
                'name': prod.name_uz,
                'name_uz': prod.name_uz,
                'name_ru': prod.name_ru,
                'name_eng': prod.name_eng,
                'price': float(prod.price),
                'stock': prod.stock,
                'description': prod.description_uz or '',
                'description_uz': prod.description_uz or '',
                'description_ru': prod.description_ru or '',
                'description_eng': prod.description_eng or '',
                'image': prod.main_image.path if prod.main_image else None,
                'category_id': prod.category.id if prod.category else None,
                'cat_name_uz': prod.category.name_uz if prod.category else '',
                'cat_name_ru': prod.category.name_ru if prod.category else '',
                'cat_name_eng': prod.category.name_eng if prod.category else ''
            }
            result.append(prod_data)
        return result

    def get_product_by_id(self, product_id):
        product = Product.available.filter(id=product_id).first()
        if product:
            return {
                'id': product.id,
                'name': product.name_uz,
                'name_uz': product.name_uz,
                'name_ru': product.name_ru,
                'name_eng': product.name_eng,
                'price': float(product.price),
                'stock': product.stock,
                'description': product.description_uz or '',
                'description_uz': product.description_uz or '',
                'description_ru': product.description_ru or '',
                'description_eng': product.description_eng or '',
                'image': product.main_image.path if product.main_image else None,
                'category_id': product.category.id if product.category else None
            }
        return None

    def get_product_for_cart(self, product_id):
        product = Product.available.select_related('category').filter(id=product_id).first()
        if product:
            return {
                'id': product.id,
                'name': product.name_uz,
                'name_uz': product.name_uz,
                'name_ru': product.name_ru,
                'name_eng': product.name_eng,
                'price': float(product.price),
                'stock': product.stock,
                'description': product.description_uz or '',
                'description_uz': product.description_uz or '',
                'description_ru': product.description_ru or '',
                'description_eng': product.description_eng or '',
                'image': product.main_image.path if product.main_image else None,
                'category_id': product.category.id if product.category else None,
                'cat_name_uz': product.category.name_uz if product.category else '',
                'cat_name_ru': product.category.name_ru if product.category else '',
                'cat_name_eng': product.category.name_eng if product.category else ''
            }
        return None


    def get_user_orders(self, user_id):
        active_orders = Order.objects.filter(user=user_id).exclude(
            status__in=[
                OrderStatus.DELIVERED,
                OrderStatus.CANCELED,
                OrderStatus.RETURNED
            ]
        ).order_by('-created_at')

        return active_orders

    def get_order_products(self, order_id):
        """Returns order details (simplified - no OrderItem)"""
        try:
            order = Order.objects.get(id=order_id)
            return {
                'id': order.id,
                'total_price': order.total_price,
                'status': order.status,
                'payment_method': order.payment_method,
                'phone_number': order.phone_number,
            }
        except Order.DoesNotExist:
            return None

