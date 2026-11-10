from django.contrib import admin
from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['stripe_payment_id', 'created_at', 'updated_at']
    search_fields = ['stripe_payment_id', 'order__id']
  
