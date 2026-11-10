from django.db import models
from tgbot.models import Order


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('succeeded', 'Muvaffaqiyatli'),
        ('failed', 'Muvaffaqiyatsiz'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    stripe_payment_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.stripe_payment_id} - Order #{self.order.id}"

