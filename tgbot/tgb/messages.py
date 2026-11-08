import bot_globals as globals
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database import Database
from tgbot.tgb.register import check_data_decorator, check_user
from tgbot.tgb.logger import logger
import bot_methods
from bot_commands import set_bot_commands
db = Database()

@check_data_decorator
def message_handler(update, context):
    message = update.message.text
    user = update.message.from_user
    state = context.user_data.get("state", 0)
    db_user = db.get_user_by_chat_id(user.id)
    if state == 0:
        check_user(update, context)
    elif state == 1:
        if not db_user["language"]:

            if message == globals.BTN_LANG_UZ:
                db.update_user_data(user.id, 'language', 1)
                logger.info(f"🌍 LANGUAGE: User {user.id} (@{user.username}) selected language: Uzbek")
                check_user(update, context)

            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id, "language", 2)
                logger.info(f"🌍 LANGUAGE: User {user.id} (@{user.username}) selected language: Russian")
                check_user(update, context)
            elif message == globals.BTN_LANG_ENG:
                db.update_user_data(user.id, "language", 1)
                logger.info(f"🌍 LANGUAGE: User {user.id} (@{user.username}) selected language: English")
                check_user(update, context)
            else:
                update.message.reply_text(
                    text=globals.TEXT_LANG_WARNING
                )
        elif not db_user["full_name"]:
            set_bot_commands(context.bot, db_user['language'], user.id)
            db.update_user_data(user.id, "full_name", message)
            logger.info(f"📝 REGISTRATION: User {user.id} (@{user.username}) registered: {message}")
            buttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['language']], request_contact=True)]
            ]
            check_user(update, context)
        elif not db_user["phone_number"]:
            # User should send contact, not text message
            buttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['language']], request_contact=True)]
            ]
            update.message.reply_text(
                text="📞 Iltimos, kontaktingizni yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
            )
        else:
            check_user(update, context)
    elif state == 2:
        if message == globals.TEXT_ORDER[db_user['language']]:
            categories = db.get_categories_by_parent()
            buttons = bot_methods.send_category_buttons(categories=categories, lang_id=db_user['language'])

            if context.user_data.get("carts",{}):
                carts = context.user_data.get("carts")
                text = f"{globals.AT_KORZINKA[db_user['language']]}:\n\n"
                lang_code = globals.LANGUAGE_CODE[db_user['language']]
                total_price = 0
                for cart, val in carts.items():
                    product = db.get_product_for_cart(int(cart))
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
                    total_price += product['price'] * val
                text += f"\n{globals.ALL[db_user['language']]}: {total_price}"
                buttons.append(
                    [InlineKeyboardButton(text=globals.BTN_KORZINKA[db_user['language']], callback_data="cart")])
                logger.info(f"🛒 ORDER: User {user.id} (@{user.username}) added product to cart, total: {total_price}")
            else:
                text =globals.TEXT_CHOOSE_CATEGORY[db_user['language']]
                logger.info(f"📂 CATEGORY: User {user.id} (@{user.username}) pressed order button")
            update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons,
                )
            )
        elif message == globals.TEXT_MY_ORDERS[db_user['language']]:
            from order_utils import show_my_orders
            show_my_orders(update, db_user)

        elif message == globals.TEXT_ABOUT_US[db_user['language']]:
            update.message.reply_text(
                text=globals.ABOUT_COMPANY[db_user['language']],
                parse_mode="HTML"
            )

        elif message == globals.TEXT_SETTINGS[db_user['language']]:
            buttons = globals.LANG_BTN
            update.message.reply_text(
                text=globals.CHOOSE_LANG,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )
            context.user_data["state"] = globals.STATES["settings"]

        elif message == globals.TEXT_HELP[db_user['language']]:
            update.message.reply_text(
                text=globals.TEXT_HELP_MENU[db_user['language']],
                parse_mode="HTML"
            )

    elif state == 3:
        if message == globals.BTN_LANG_UZ:
            db.update_user_data(db_user['chat_id'], "language", 1)
            context.user_data["state"] = globals.STATES["reg"]
            check_user(update, context)

        elif message == globals.BTN_LANG_RU:
            db.update_user_data(db_user['chat_id'], "language", 2)
            context.user_data["state"] = globals.STATES["reg"]
            check_user(update, context)

        elif message == globals.BTN_LANG_ENG:
            db.update_user_data(db_user['chat_id'], 'language', 3)
            context.user_data["state"] = globals.STATES["reg"]
            check_user(update, context)
        else:
            update.message.reply_text(
                text=globals.TEXT_LANG_WARNING
            )
    else:
        update.message.reply_text("Salom")


