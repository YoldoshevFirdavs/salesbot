from telegram import BotCommand, BotCommandScopeChat

def set_bot_commands(bot, language, chat_id):
    commands = {
        1: [
            BotCommand("start", "Botni ishga tushirish / Qayta boshlash"),
            BotCommand("main_menu", "Asosiy menyu"),
            BotCommand("my_orders", "Mening buyurtmalarim")
        ],
        2: [
            BotCommand("start", "Запустить бота / Перезапустить"),
            BotCommand("main_menu", "Главное меню"),
            BotCommand("my_orders", "Мои заказы")
        ],
        3: [
            BotCommand("start", "Start bot / Restart"),
            BotCommand("main_menu", "Main menu"),
            BotCommand("my_orders", "My orders")
        ]
    }

    selected_commands = commands.get(language, commands[1])

    bot.set_my_commands(
        selected_commands,
        scope=BotCommandScopeChat(chat_id=chat_id)
    )