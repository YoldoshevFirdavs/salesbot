import re

import phonenumbers
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumbers import PhoneNumberFormat


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def normalize_phone(phone_number):
        """
        Telefon raqamdagi ortiqcha belgilarni (probel, tire, qavs) olib tashlaydi,
        faqat raqamlar va boshidagi '+' belgisini qoldiradi.
        """
        if not phone_number:
            return None
        return re.sub(r"[^\d+]", "", phone_number)

    def _create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqami kiritilishi shart!")

        phone_number = self.normalize_phone(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            phone_number=phone_number, password=password, **extra_fields
        )

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not phone_number:
            raise ValueError("Superuser must have a phone number")
        return self._create_user(
            phone_number=phone_number, password=password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=32, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    telegram_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(
        upload_to="users_profile_avatars/", blank=True, null=True
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name or self.email or self.phone_number}"

    def get_display_name(self):
        return self.full_name if self.full_name else self.email

    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/images/default/default_avatar.png"

    def clean_phone_number(self):
        if self.phone_number:
            try:
                parsed_number = phonenumbers.parse(
                    self.phone_number, settings.PHONENUMBER_DEFAULT_REGION
                )
                if phonenumbers.is_valid_number(parsed_number):
                    self.phone_number = phonenumbers.format_number(
                        parsed_number, PhoneNumberFormat.E164
                    )
                else:
                    self.phone_number = None  # Invalidate if not a valid number
            except phonenumbers.phonenumberutil.NumberParseException:
                self.phone_number = None  # Invalidate if parsing fails

    def save(self, *args, **kwargs):
        self.clean_phone_number()
        super().save(*args, **kwargs)
