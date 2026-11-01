from rest_framework import serializers

from tgbot.models import Category, ProductImage, Product, CartItem, Cart, Order, OrderItem

DEFAULT_AVATAR_URL = "/static/images/default/default_avatar.png"
DEFAULT_PRODUCT_URL = "/static/images/default/default_product.png"

class RecursiveField(serializers.Serializer):
    """
    Recursive serializer for nested categories.
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "is_default", "children"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "is_primary"]


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source="category.name")
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "price",
            "main_image",
            "image_url",
            "stock",
        ]

    def get_image_url(self, obj):
        if (
            obj.main_image
            and hasattr(obj.main_image, "url")
            and hasattr(obj.main_image, "name")
            and obj.main_image.name
        ):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return DEFAULT_PRODUCT_URL


class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source="product", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_details", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "price",
            "stock",
            "main_image",
            "main_image_url",
            "images",
            "description",

        ]

    def get_main_image_url(self, obj):
        if (
            obj.main_image
            and hasattr(obj.main_image, "url")
            and hasattr(obj.main_image, "name")
            and obj.main_image.name
        ):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return DEFAULT_PRODUCT_URL



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "grand_total", "created_at"]

    def get_grand_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

class CartSummarySerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total", "created_at"]

    def get_grand_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())




class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price_at_order"]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # 1. Avval buyurtmani boshlang'ich narx 0 bilan yaratamiz (yoki hisoblab yaratamiz)
        order = Order.objects.create(user=user, total_price=0, **validated_data)

        total_price = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price * quantity
            total_price += price

            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)

        # 2. Hisoblangan umumiy narxni order'ga yozib saqlaymiz
        order.total_price = total_price
        order.save()

        return order


class OrderListSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    short_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "short_address", "created_at"]
        read_only_fields = [
            "id",
            "status",
            "total_price",
            "short_address",
            "created_at",
        ]

    def get_total_price(self, obj):
        if hasattr(obj, "total_price") and obj.total_price is not None:
            return obj.total_price
        return sum(item.price_at_order * item.quantity for item in obj.order_items.all())

    def get_short_address(self, obj):
        return (obj.address[:80] + "...") if obj.address and len(obj.address) > 80 else obj.address


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    delivery_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_items",
            "total_price",
            "status",
            "address",
            "created_at",
            "delivery_details",
        ]
        read_only_fields = [
            "id",
            "user",
            "order_items",
            "total_price",
            "created_at",
            "delivery_details",
        ]
    
    def get_delivery_details(self, obj):
        return {
            "phone_number": obj.phone_number,
            "payment_method": obj.payment_method,
            "accepted_at": obj.accepted_at,
            "delivered_at": obj.delivered_at,
        }












