from django.urls import path
from .views import (
    checkout,
    payment_success,
    StripeWebhookView,
)

app_name = 'payment'

urlpatterns = [
    path("webhook/", StripeWebhookView.as_view(), name="webhook"),
]
