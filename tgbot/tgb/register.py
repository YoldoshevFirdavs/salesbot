from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from database import Database
import bot_globals as globals
from bot_methods import send_main_menu
from logger import logger
from tgbot.tgb.bot_commands import set_bot_commands

db = Database()

def check_user(update, context):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    
    first_time = not db_user
    if first_time:
        logger.info(f"✅ NEW USER: User {user.id} (@{user.username}) started bot for the first time")
    else:
        logger.info(f"🔄 RETURNING USER: User {user.id} (@{user.username}) restarted bot")

    if not db_user:
        db.create_user(user.id, user.id)
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=globals.LANG_BTN,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]
    elif not db_user["language"]:
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=globals.LANG_BTN,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["full_name"]:
        set_bot_commands(context.bot, db_user['language'], user.id)
        update.message.reply_text(
            text=globals.TEXT_ENTER_FULL_NAME[db_user['language']],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["phone_number"]:
        buttons = [
            [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['language']], request_contact=True)]
        ]
        update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT[db_user['language']],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]
    else:
        send_main_menu(context, user.id, db_user["language"])
        context.user_data["state"] = globals.STATES["menu"]



def check_data_decorator(func):
    def inner(update, context):
        user = update.message.from_user
        db_user = db.get_user_by_chat_id(user.id)
        state = context.user_data.get("state", 0)

        if state != globals.STATES['reg']:

            if not db_user:
                db.create_user(user.id, user.id)
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=globals.LANG_BTN,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]
            elif not db_user["language"]:
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=globals.LANG_BTN,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["full_name"]:
                set_bot_commands(context.bot, db_user['language'], user.id)
                update.message.reply_text(
                    text=globals.TEXT_ENTER_FULL_NAME[db_user['language']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["phone_number"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['language']], request_contact=True)]
                ]
                update.message.reply_text(
                    text=globals.TEXT_ENTER_CONTACT[db_user['language']],
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]
            else:
                return func(update, context)

            return False

        else:
            return func(update, context)
    return inner
