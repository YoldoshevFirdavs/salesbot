import os
import sys
import django

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from database import Database
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from register import check_user
from messages import message_handler
from inlines import inline_handler
from config.settings import BOT_TOKEN
import bot_globals as globals
import bot_methods
from bot_commands import set_bot_commands
from telegram import Update

TOKEN = BOT_TOKEN
db = Database()

def start_handler(update, context):
    check_user(update, context)

def main_menu_handler(update: Update, context: CallbackContext):
    check_user(update, context)

def my_orders_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    db_user = db.get_user_by_chat_id(user.id)
    if not db_user:
        update.message.reply_text("Iltimos, avval /start buyrug'ini bosing.")
        return
    lang = db_user.get('language', 1)
    orders = db.get_user_orders(db_user.get('id'))
    orders = db.get_user_orders(db_user['id'])

    if not orders or orders.count() == 0:
        update.message.reply_text(
            text="❌ Sizda faol buyurtmalar yo'q",
        )
    else:
        text = "📦 <b>Sizning buyurtmalaringiz:</b>\n\n"
        for order in orders:
            text += "🆔 Buyurtma #{}\n".format(order.id)
            text += "💰 Summa: {:,.0f} so'm\n".format(float(order.total_price))
            text += "📅 Sana: {}\n".format(order.created_at.strftime('%d.%m.%Y %H:%M'))
            text += "📊 Holat: {}\n".format(order.get_status_display())
            text += "────────────────\n\n"

        update.message.reply_text(
            text=text,
            parse_mode='HTML',

        )

def contact_handler(update, context):
    message = update.message.contact.phone_number
    user = update.message.from_user
    db.update_user_data(user.id, "phone_number", message)
    check_user(update, context)

def location_handler(update, context):
    ADMIN_ID = 7672818786  # Replace with your admin telegram ID
    
    db_user = db.get_user_by_chat_id(update.message.from_user.id)
    location = update.message.location
    payment_type = context.user_data.get("payment_type", 1)
    
    address = "Lat: {}, Lon: {}".format(location.latitude, location.longitude)
    phone_number = db_user.get('phone_number', 'Nomalum')
    payment_method = "cash" if payment_type == 1 else "card"
    
    db.create_order(db_user['id'], context.user_data.get("carts", {}), payment_method, address, phone_number)

    # Prepare order details
    text = ""
    total_price = 0
    
    if context.user_data.get("carts", {}):
        carts = context.user_data.get("carts")
        lang_code = globals.LANGUAGE_CODE.get(db_user['language'], 'uz')
        
        for cart_id, quantity in carts.items():
            product = db.get_product_for_cart(int(cart_id))
            if product:
                item_price = product['price'] * quantity
                product_name = product.get('name_' + lang_code, product.get('name_uz', 'Product'))
                text += "{} x {} - {:,.0f} so'm\n".format(quantity, product_name, item_price)
                total_price += item_price
        
        text += "\n<b>Jami:</b> {:,.0f} so'm".format(total_price)

    # Send order to admin
    payment_text = "Naqd pul" if payment_method == 'cash' else "Karta"
    admin_message = (
        "<b>YANGI BUYURTMA!</b>\n\n"
        "<b>Mijoz:</b> {}\n"
        "<b>Telefon:</b> {}\n"
        "<b>To'lov:</b> {}\n\n"
        "<b>Mahsulotlar:</b>\n{}"
    ).format(
        db_user.get('full_name', 'Nomalum'),
        phone_number,
        payment_text,
        text
    )
    
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message,
        parse_mode='HTML'
    )
    
    context.bot.send_location(
        chat_id=ADMIN_ID,
        latitude=float(location.latitude),
        longitude=float(location.longitude)
    )
    
    # Clear cart and payment info
    context.user_data.pop("carts", None)
    context.user_data.pop("payment_type", None)
    
    # Send success message to user
    update.message.reply_text(
        text="Buyurtmangiz qabul qilindi!\n\nTez orada operator siz bilan bog'lanadi."
    )
    
    bot_methods.send_main_menu(context, update.message.from_user.id, db_user['language'])

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('main_menu', main_menu_handler))
    dispatcher.add_handler(CommandHandler('my_orders', my_orders_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
