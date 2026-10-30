from django.conf import settings
from django.db import models
from django.db.models import Q

class ProductManager(models.Manager):
    def search(self, query):
        return self.filter(Q(name__icontains=query) | Q(description__icontains=query)).distinct()

class ProductAvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, stock_gt=0)

    def search(self, query):
        return self.get_queryset().filter(Q(name__icontains=query) | Q(description__icontains=query)).distinct()

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="medicines")

    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    description = models.CharField(max_length=500)
    main_image = models.ImageField(upload_to="products/main/", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()
    available = ProductAvailableManager()

    def __str__(self):
        return self.name

    def reduce_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            self.save()
            return True
        return False

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

class ProductImage(models.Model):
    medicine = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    is_primary = models.BooleanField(default=False)

class OrderStatus(models.TextChoices):
    """Order status state machine"""

    PENDING = "Pending", "Pending"
    PROCESSING = "Processing", "Processing"
    READY_FOR_DELIVERY = "Ready for Delivery", "Ready for Delivery"
    ACCEPTED = "Accepted", "Accepted"
    PICKED_UP = "Picked Up", "Picked Up"
    ON_THE_WAY = "On The Way", "On The Way"
    ARRIVED = "Arrived", "Arrived"
    DELIVERED = "Delivered", "Delivered"
    CANCELED = "Canceled", "Canceled"
    RETURNED = "Returned", "Returned"

class Cart(models.Model):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE, related_name="user_cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name or self.user.phone_number} savatchasi"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} ta)"





class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, help_text="Order status"
    )
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=20, blank=False, null=False, help_text="Ixtiyoriy telefon raqami. Yetkazib berish uchun ishlatiladi."
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ("cash", "Naqd pul"),
            ("card", "Karta"),
        ],
        default="card",
        help_text="To'lov usuli",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True, help_text="When driver accepted the order")

    def __str__(self):
        return f"Order #{self.id} - {self.user.full_name or self.user.phone_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name if self.product else 'Deleted'} x {self.quantity}"








