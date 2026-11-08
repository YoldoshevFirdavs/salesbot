from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
import bot_globals as globals
from tgbot.tgb.logger import logger

def send_main_menu(context, chat_id, lang_id, message_id=None):
    buttons = [
        [KeyboardButton(text=globals.TEXT_ORDER[lang_id])],
        [KeyboardButton(text=globals.TEXT_MY_ORDERS[lang_id]), KeyboardButton(text=globals.TEXT_ABOUT_US[lang_id])],
        [KeyboardButton(text=globals.TEXT_SETTINGS[lang_id]), KeyboardButton(text=globals.TEXT_HELP[lang_id])]
    ]
    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        logger.info(f"🏠 MAIN MENU: Sent to user {chat_id}, language: {lang_id}")


def send_category_buttons(categories, lang_id):
    buttons = []
    lang_code = globals.LANGUAGE_CODE[lang_id]

    row = []
    for index, category in enumerate(categories):
        btn = InlineKeyboardButton(
            text=category[f'name_{lang_code}'],
            callback_data=f"category_{category['id']}"
        )
        row.append(btn)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return buttons


def send_product_buttons(products, lang_id):
    buttons = []
    row = []
    for i in range(len(products)):
        row.append(
            InlineKeyboardButton(
                text=products[i][f'name_{globals.LANGUAGE_CODE[lang_id]}'],
                callback_data=f"category_product_{products[i]['id']}"
            )
        )

        if len(row) == 2 or (len(products) % 2 == 1 and i == len(products) - 1):
            buttons.append(row)
            row = []

    return buttons
