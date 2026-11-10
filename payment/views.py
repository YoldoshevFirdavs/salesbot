import logging
import stripe
import asyncio
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .exceptions import (
    OrderNotFoundException,
    StripeException,
    WebhookSignatureException,
)
from tgbot.models import Order

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request, order_id):
    """Creates Stripe Checkout Session - redirects to Stripe hosted page"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect("/")
    
    if order.status == "Accepted":
        return redirect("/")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(float(order.total_price) * 100),
                        "product_data": {
                            "name": f"Buyurtma #{order.id}",
                            "description": f"Jami: {order.total_price} so'm",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(f"/payment-success/{order.id}/"),
            cancel_url=request.build_absolute_uri(f"/checkout/{order.id}/"),
            metadata={
                "order_id": str(order.id),
                "user_id": str(order.user.id) if order.user else "anonymous",
            },
        )
        
        logger.info(f"Stripe Checkout Session created for order {order.id}")
        return redirect(checkout_session.url)
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        return redirect("/")


def payment_success(request, order_id):
    """Payment success page"""
    try:
        order = Order.objects.get(id=order_id)
        if order.status != "Accepted":
            order.status = "Accepted"
            order.save()
            logger.info(f"Order {order_id} Accepted")
    except Order.DoesNotExist:
        pass
    
    return render(request, "payment_success.html", {"order_id": order_id})


async def send_telegram_notification(chat_id, order):
    """Send Telegram notification async"""
    try:
        from telegram import Bot
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        message_text = (
            f"✅ <b>To'lov muvaffaqiyatli!</b>\n\n"
            f"🆔 Buyurtma raqami: #{order.id}\n"
            f"💰 Summa: {order.total_price:,.0f} so'm\n"
            f"📊 Holat: Qabul qilindi\n\n"
            f"Tez orada sizning buyurtma tayyorlanadi!"
        )
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
            parse_mode='HTML'
        )
        logger.info(f"Telegram notification sent to user {chat_id} for order {order.id}")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        webhook_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)

        if not webhook_secret:
            return Response(
                {"error": "Webhook secret not configured"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(
                {"error": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if event.get("type") == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session.get("metadata", {}).get("order_id")

            if order_id:
                try:
                    order = Order.objects.get(id=int(order_id))
                    order.status = "Accepted"
                    order.save(update_fields=["status"])

                    Payment.objects.create(
                        order=order,
                        stripe_payment_id=session.get("id", ""),
                        amount=order.total_price,
                        currency="usd",
                        status="succeeded",
                    )

                    logger.info(f"Payment succeeded for order {order.id}")

                    # Send Telegram notification to user
                    if order.user and order.user.chat_id:
                        try:
                            # Run async notification
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            loop.run_until_complete(
                                send_telegram_notification(order.user.chat_id, order)
                            )
                            loop.close()
                        except Exception as e:
                            logger.error(f"Failed to send Telegram notification: {e}")

                except Order.DoesNotExist:
                    logger.error(f"Order {order_id} not found")

        return Response({"status": "ok"}, status=status.HTTP_200_OK)
