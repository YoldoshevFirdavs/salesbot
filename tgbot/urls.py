from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tgbot.views import ProductViewSet, CategoryViewSet, OrderViewSet, CartViewSet
from users.views import CustomUserViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
