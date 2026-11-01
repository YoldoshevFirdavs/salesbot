import phonenumbers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Default image URLs
DEFAULT_AVATAR_URL = "/static/images/default/default_avatar.png"
DEFAULT_PRODUCT_URL = "/static/images/default/default_product.png"

from django.conf import settings
from django.contrib.auth import get_user_model
from phonenumbers import PhoneNumberFormat
from PIL import Image
from rest_framework import serializers

from .models import CustomUser

User = get_user_model()

def validate_image_file(file):
    """Validate that file is a valid image format."""
    try:
        img = Image.open(file)
        img.verify()
    except IOError as e:
        raise serializers.ValidationError(f"Fayl o'qilmadi yoki corrupt: {str(e)[:50]}")
    except Exception as e:
        raise serializers.ValidationError(f"Rasm tekshirilmadi: {type(e).__name__}")
    return file

class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, data):
        if isinstance(data, (list, tuple)):
            data = data[0] if data else ""
        data = str(data).strip()
        if not data:
            return None

        if len(data) == 9 and data.isdigit() and not data.startswith("+"):
            data = f"+{settings.PHONENUMBER_DEFAULT_REGION_CODE}{data}"

        try:
            parsed_number = phonenumbers.parse(data, settings.PHONENUMBER_DEFAULT_REGION)
            if not phonenumbers.is_valid_number(parsed_number):
                parsed_number = phonenumbers.parse(data)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise serializers.ValidationError("Telefon raqami noto‘g‘ri.")

            return phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Telefon raqami noto‘g‘ri formatda.")
        except Exception:
            raise serializers.ValidationError("Telefon raqamini tekshirishda xato yuz berdi.")


class CustomUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    phone_number = PhoneNumberField(required=True, allow_blank=False, allow_null=False)
    avatar = serializers.ImageField(validators=[validate_image_file], required=False, allow_null=True)
    telegram_id = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "phone_number",
            "email",
            "full_name",
            "telegram_id",
            "address",
            "avatar",
            "avatar_url",
            "is_verified",
            "date_joined",
            "is_staff",
        ]
        read_only_fields = [
            "is_verified",
            "date_joined",
            "is_staff",
        ]
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True, "allow_null": True},
            "full_name": {"required": False, "allow_blank": True},
            "address": {"required": False, "allow_blank": True},
            "telegram_id": {"required": False, "allow_blank": True, "allow_null": True},
        }
    def get_avatar_url(self, obj):
        if hasattr(obj, "seller") and obj.seller:
            return obj.seller.get_avatar_url
        if obj.avatar and hasattr(obj.avatar, "name") and obj.avatar.name:
            return obj.avatar.url
        return DEFAULT_AVATAR_URL
    def validate_telegram_id(self, value):
        """Validate Telegram ID format and uniqueness"""
        if not value:
            return value  # Allow empty telegram_id

        # Telegram ID should be numeric or start with @
        value = value.strip()
        if value.startswith("@"):
            # Username format: @username
            username = value[1:]
            if not username.replace("_", "").isalnum() or len(username) < 5:
                raise serializers.ValidationError(
                    "Telegram username noto'g'ri formatda. Namuna: @username (eng kamida 5 ta belgi)"
                )
        else:
            # Numeric ID format
            if not value.isdigit():
                raise serializers.ValidationError(
                    "Telegram ID raqamlar bilan yoki @username ko'rinishida bo'lishi kerak. Namuna: 123456789 yoki @username"
                )
            if len(value) < 5 or len(value) > 20:
                raise serializers.ValidationError("Telegram ID 5 dan 20 ta raqamdan iborat bo'lishi kerak.")

        # Check uniqueness (excluding current user if updating)
        if self.instance and value:
            if CustomUser.objects.exclude(id=self.instance.id).filter(telegram_id=value).exists():
                raise serializers.ValidationError("Bu Telegram ID allaqachon ishlatilgan.")
        elif not self.instance and value:  # For create operations
            if CustomUser.objects.filter(telegram_id=value).exists():
                raise serializers.ValidationError("Bu Telegram ID allaqachon ishlatilgan.")

        return value
    def validate_phone_number(self, value):
        if not value:
            return value  # Allow empty phone number if not required
        try:
            parsed_number = phonenumbers.parse(value, settings.PHONENUMBER_DEFAULT_REGION)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Telefon raqami noto'g'ri formatda.")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Telefon raqami noto'g'ri formatda.")

        if self.instance and value:
            if CustomUser.objects.exclude(id=self.instance.id).filter(phone_number=value).exists():
                raise serializers.ValidationError("Bu telefon raqami allaqachon mavjud.")
        elif not self.instance and value:  # For create operations
            if CustomUser.objects.filter(phone_number=value).exists():
                raise serializers.ValidationError("Bu telefon raqami allaqachon mavjud.")
        return value

    def validate_email(self, value):
        if value == "":
            return None  # Allow empty email if not required
        if self.instance and value:
            if CustomUser.objects.exclude(id=self.instance.id).filter(email=value).exists():
                raise serializers.ValidationError("Bu Gmail manzili allaqachon mavjud.")
        elif not self.instance and value:  # For create operations
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Bu Gmail manzili allaqachon mavjud.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        from django.db import transaction

        password = validated_data.pop("password", None)
        avatar = validated_data.pop("avatar", None)

        try:
            with transaction.atomic():
                # Update non-sensitive fields
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)

                if password:
                    instance.set_password(password)

                # Update avatar - set on both user and seller for consistency
                if avatar:
                    instance.avatar = avatar  # Always set on user
                    if hasattr(instance, "seller") and instance.seller:
                        instance.seller.avatar = avatar
                        instance.seller.save()

                instance.save()
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"User profile update failed for user {instance.id}: {str(e)}")
            raise

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Username o'rniga phone_number maydonini talab qiladigan qilamiz
    username_field = 'phone_number'

    def validate(self, attrs):
        # Ota klassdagi tekshiruvlarni chaqiramiz
        data = super().validate(attrs)

        # Qo'shimcha ravishda user haqida ma'lumotlarni ham token bilan birga qaytarishimiz mumkin (ixtiyoriy)
        data['user_id'] = self.user.id
        data['phone_number'] = self.user.phone_number
        data['is_staff'] = self.user.is_staff

        return data


