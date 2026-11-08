# Order utility functions
from telegram import KeyboardButton, ReplyKeyboardMarkup
import bot_globals as globals
from database import Database

db = Database()

def show_my_orders(update, db_user):
    """
    Display user's orders. Works for both messages.py and runbot.py
    
    Args:
        update: Telegram update object
        db_user: User data from database
    """
    orders = db.get_user_orders(db_user['id'])
    lang = db_user.get('language', 1)

    main_buttons = [
        [KeyboardButton(text=globals.TEXT_ORDER[lang])],
        [KeyboardButton(text=globals.TEXT_MY_ORDERS[lang])],
    ]
    if not orders or orders.count() == 0:
        update.message.reply_text(
            text=globals.NO_ZAKAZ.get(lang, globals.NO_ZAKAZ[1]),
            reply_markup=ReplyKeyboardMarkup(
                keyboard=main_buttons,
                resize_keyboard=True
            )
        )
        return
    title_text = {
        1: "📦 <b>Sizning buyurtmalaringiz:</b>\n\n",
        2: "📦 <b>Ваши заказы:</b>\n\n",
        3: "📦 <b>Your orders:</b>\n\n"
    }
    text = title_text.get(lang, title_text[1])
    for order in orders:
        order_id_text = {
            1: "🆔 Buyurtma #{}",
            2: "🆔 Заказ #{}",
            3: "🆔 Order #{}"
        }
        text += order_id_text.get(lang, order_id_text[1]).format(order.id) + "\n"
        total_text = {
            1: "💰 Summa: {:,.0f} so'm",
            2: "💰 Сумма: {:,.0f} сум",
            3: "💰 Total: {:,.0f} som"
        }
        text += total_text.get(lang, total_text[1]).format(float(order.total_price)) + "\n"
        date_text = {
            1: "📅 Sana: {}",
            2: "📅 Дата: {}",
            3: "📅 Date: {}"
        }
        text += date_text.get(lang, date_text[1]).format(
            order.created_at.strftime('%d.%m.%Y %H:%M')
        ) + "\n"
        status_text = {
            1: "📊 Holat: {}",
            2: "📊 Статус: {}",
            3: "📊 Status: {}"
        }
        text += status_text.get(lang, status_text[1]).format(
            order.get_status_display()
        ) + "\n"
        text += "────────────────\n\n"
    update.message.reply_text(
        text=text,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=main_buttons,
            resize_keyboard=True
        )
    )
