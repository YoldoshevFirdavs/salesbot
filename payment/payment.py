import logging
import stripe
from django.conf import settings

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(order_id, amount, currency='usd', description=None):
    """
    Creates a Stripe Payment Intent for the order
    Returns: (client_secret, error)
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata={'order_id': order_id},
            description=description or f"Order {order_id}"
        )
        return intent.client_secret, None
    except stripe.error.StripeError as e:
        logger.error(f"Stripe Payment Intent creation failed: {e}")
        return None, str(e)

def verify_payment(payment_id):
    """
    Verifies if a payment was successful
    Returns: (is_success, payment_data)
    """
    try:
        intent = stripe.PaymentIntent.retrieve(payment_id)
        return intent.status == 'succeeded', intent
    except stripe.error.StripeError as e:
        logger.error(f"Stripe verification failed: {e}")
        return False, None

def handle_webhook(payload, sig_header):
    """
    Handles Stripe webhooks
    Returns: (event, error)
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return event, None
    except ValueError as e:
        logger.error(f"Invalid webhook payload: {e}")
        return None, str(e)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid webhook signature: {e}")
        return None, str(e)
