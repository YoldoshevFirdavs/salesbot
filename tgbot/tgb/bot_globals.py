from telegram import InlineKeyboardButton, KeyboardButton

CHOOSE_LANG = (
    "🇺🇿 Iltimos, botdan foydalanish uchun muloqot tilini tanlang:\n\n"
    "🇷🇺 Пожалуйста, выберите язык общения для использования бота:\n\n"
    "🇬🇧 Please select your preferred language to use the bot:"
)
TEXT_LANG_WARNING = "Iltimos tillardan birini tanlang!\nПожалуйста, выберите один из языков!\nPlease choose one language!"
# Tugmalar uchun matnlar:
BTN_LANG_UZ = "🇺🇿 O'zbek tili"
BTN_LANG_RU = "🇷🇺 Русский язык"
BTN_LANG_ENG= "🇬🇧 English language"
WELCOME_TEXT = {
1:(
    "✨ **Assalomu alaykum! Xush kelibsiz!**\n\n"
    "🛍 Bizning onlayn do'konimiz orqali siz o'zingizga kerakli mahsulotlarni osongina buyurtma qilishingiz mumkin."
), 2:(
    "✨ **Здравствуйте! Добро пожаловать!**\n\n"
    "🛍 Через наш интернет-магазин вы можете легко заказать необходимые вам товары."
), 3:(
    "✨ **Hello! Welcome!**\n\n"
    "🛍 Through our online store, you can easily order the products you need."
)}
LANG_BTN = [
            [KeyboardButton(text=BTN_LANG_UZ), KeyboardButton(text=BTN_LANG_RU), KeyboardButton(text=BTN_LANG_ENG)]
]
BTN_SEND_CONTACT = {
    1: "Yuborish",
    2: "Отправить",
    3: "Send"
}
TEXT_PRODUCT_PRICE = {
    1: "Narx:",
    2: "Цена:",
    3: "Price"
}
TEXT_PRODUCT_DESC = {
    1: "Tarkibi:",
    2: "Состав:",
    3: "Contents:"
}
SUM = {
    1: "so'm",
    2: "сум",
    3: "som"
}
NO_ZAKAZ = {
    1: "Siz hali birorta buyurtma bermadingiz!",
    2: "Вы еще не разместили ни одного заказа!",
    3: "You haven't ordered anything!"
}
ALL = {
    1: "Jami",
    2: "Все",
    3: "Total"
}
TEXT_ENTER_CONTACT = {
    1: "❌ Iltimos, raqamni qo'lda yozmang!\nFaqat pastdagi **<<Yuborish>>** tugmasini bosing:",
    2: "❌ Пожалуйста, не вводите номер вручную!\nНажмите только кнопку **<<Отправить>>** ниже:",
    3: "❌ Please do not type the number manually!\nPress only the **<<Send>>** button below:"
}

TEXT_CHOOSE_CATEGORY = {
    1: "📦 Kategoriyalarni tanlang",
    2: "📦 Выберите категории",
    3: "📦 Choose categories"
}
STATES = {
 'reg':1,
 'menu':2,
 'settings':3
}

BTN_KORZINKA = {
    1: "🛍 Xarid qilish",
    2: "🛍 Покупка товаров",
    3: "🛍 Buy"
}
AT_KORZINKA = {
    1: "Savatchada",
    2: "В корзине",
    3: "In cart"
}
LANGUAGE_CODE = {
    1: "uz",
    2: "ru",
    3: "eng"
}
SEND_PHONE_NUMBER = {
    1:"Yuborish",
    2:"Отправлять",
    3:"Send"
}

TEXT_ENTER_FULL_NAME = {
    1: "Iltimos, to'liq ismingizni kiriting!",
    2: "Пожалуйста, введите ваше полное имя!",
    3: "Please enter your full name!"
}

TEXT_MAIN_MENU = {
    1: "🏠 Asosiy menyu",
    2: "🏠 Главное меню",
    3: "🏠 Main menu"
}
TEXT_ABOUT_US = {
    1:"📄 Biz haqimizda",
    2:"📄 O нас",
    3:"📄 About us"
}
TEXT_SETTINGS = {
    1: "⚙️ Sozlamalar",
    2: "⚙️ Настройки",
    3: "⚙️ Settings"
}
TEXT_HELP_MENU = {
    1: (
        "<b>Botdan foydalanish bo'yicha yordam:</b>\n\n"
        "Buyurtma berish, mahsulotlarni tanlash yoki savatni boshqarish bo'yicha savollaringiz bo'lsa, "
        "biz bilan bog'lanishingiz mumkin:\n\n"
        "📞 Telegram: <a href=\"https://t.me/firdavsy2011\">@firdavsy2011</a>\n"
        "📧 Email: <a href=\"mailto:firdavsyoldoshevpython@gmail.com\">firdavsyoldoshevpython@gmail.com</a>"
    ),
    2: (
        "<b>Помощь по использованию бота:</b>\n\n"
        "Если у вас возникли вопросы по оформлению заказа, выбору товаров или управлению корзиной, "
        "вы можете связаться с нами:\n\n"
        "📞 Telegram: <a href=\"https://t.me/firdavsy2011\">@firdavsy2011</a>\n"
        "📧 Email: <a href=\"mailto:firdavsyoldoshevpython@gmail.com\">firdavsyoldoshevpython@gmail.com</a>"
    ),
    3: (
        "<b>Help & Support:</b>\n\n"
        "If you have any questions regarding orders, product selection, or managing your cart, "
        "feel free to contact us:\n\n"
        "📞 Telegram: <a href=\"https://t.me/firdavsy2011\">@firdavsy2011</a>\n"
        "📧 Email: <a href=\"mailto:firdavsyoldoshevpython@gmail.com\">firdavsyoldoshevpython@gmail.com</a>"
    )
}
TEXT_ORDER = {
    1:"🛒 Buyurtma qilish",
    2:"🛒 Заказать",
    3:"🛒 Order"
}
TEXT_PRICE = {
    1:"Narx",
    2:"Цена",
    3:"Price"
}
TEXT_MY_ORDERS = {
    1:"🛍 Buyurtmalarim",
    2:"🛍 Мои заказы",
    3:"🛍 My orders"
}

# My orders page texts
TEXT_MY_ORDERS_TITLE = {
    1: "📦 <b>Sizning buyurtmalaringiz:</b>\n\n",
    2: "📦 <b>Ваши заказы:</b>\n\n",
    3: "📦 <b>Your orders:</b>\n\n"
}

TEXT_NO_ORDERS = {
    1: "❌ Sizda faol buyurtmalar yo'q",
    2: "❌ У вас нет активных заказов",
    3: "❌ You have no active orders"
}

TEXT_ORDER_ID = {
    1: "🆔 Buyurtma #{}",
    2: "🆔 Заказ #{}",
    3: "🆔 Order #{}"
}

TEXT_ORDER_TOTAL = {
    1: "💰 Summa: {:,.0f} so'm",
    2: "💰 Сумма: {:,.0f} сум",
    3: "💰 Total: {:,.0f} som"
}

TEXT_ORDER_DATE = {
    1: "📅 Sana: {}",
    2: "📅 Дата: {}",
    3: "📅 Date: {}"
}

TEXT_ORDER_STATUS = {
    1: "📊 Holat: {}",
    2: "📊 Статус: {}",
    3: "📊 Status: {}"
}
TEXT_HELP = {
    1:"❓ Yordam",
    2:"❓ Помощь",
    3:"❓ Help"
}
BTN_BACK = {
    1:"Orqaga",
    2:"Назад",
    3:"Back"
}


ABOUT_COMPANY = {
    1: (
        "<b>🏢 Biz haqimizda</b>\n\n"
        "✨ Hurmatli mijoz! Bizning onlayn do'konimiz sizning vaqtingizni tejash, kundalik ehtiyojlaringizni eng qulay va ishonchli tarzda ta'minlash maqsadida tashkil etilgan.\n\n"
        "🚀 <b>Bizning afzalliklarimiz:</b>\n"
        "• 🛍 Keng assortimentdagi sifatli mahsulotlar\n"
        "• ⚡️ Tezkor va o'z vaqtida yetkazib berish xizmati\n"
        "• 🤝 Har bir mijozga alohida yondashuv\n"
        "• 💳 Qulay va xavfsiz to'lov usullari\n\n"
        "🎯 Bizning asosiy maqsadimiz — sizning ishonchingizni oqlash va xaridlaringizni yanada yoqimli qilish!\n\n"
        "📞 Savollar yoki takliflar bo'yicha doimo aloqadamiz. Bizni tanlaganingiz uchun rahmat! ❤️"
    ),
    2: (
        "<b>🏢 О нас</b>\n\n"
        "✨ Уважаемый клиент! Наш интернет-магазин создан для того, чтобы сэкономить ваше время и обеспечить вас необходимыми товарами самым удобным и надежным способом.\n\n"
        "🚀 <b>Наши преимущества:</b>\n"
        "• 🛍 Широкий ассортимент качественных товаров\n"
        "• ⚡️ Быстрая и своевременная доставка\n"
        "• 🤝 Индивидуальный подход к каждому клиенту\n"
        "• 💳 Удобные и безопасные способы оплаты\n\n"
        "🎯 Наша главная цель — оправдать ваше доверие и сделать ваши покупки приятными!\n\n"
        "📞 Мы всегда на связи по любым вопросам и предложениям. Спасибо, что выбрали нас! ❤️"
    ),
    3: (
        "<b>🏢 About Us</b>\n\n"
        "✨ Dear customer! Our online store is designed to save your time and provide you with the necessary products in the most convenient and reliable way.\n\n"
        "🚀 <b>Our advantages:</b>\n"
        "• 🛍 A wide range of quality products\n"
        "• ⚡️ Fast and punctual delivery service\n"
        "• 🤝 Individual approach to every customer\n"
        "• 💳 Convenient and secure payment methods\n\n"
        "🎯 Our main goal is to earn your trust and make your shopping experience delightful!\n\n"
        "📞 We are always in touch for any questions or suggestions. Thank you for choosing us! ❤️"
    )
}

BTN_SEND_LOCATION = {
    1:"📍 Lokatsiya jo'nating",
    2:"📍 Отправить местоположение",
    3:"📍 Send location"
}

# Payment methods
PAYMENT_METHOD = {
    1: {"uz": "Naqd pul", "ru": "Наличные", "eng": "Cash"},
    2: {"uz": "Karta", "ru": "Карта", "eng": "Card"}
}

PAYMENT_BTN_TEXT = {
    1: "Naqd pul",  # For button display
    2: "Karta"
}

PAYMENT_BTN_TEXT_RU = {
    1: "Наличные",
    2: "Карта"
}

PAYMENT_BTN_TEXT_ENG = {
    1: "Cash",
    2: "Card"
}

# Combined for all languages
BTN_PAY_CASH = {
    1: "Naqd pul",
    2: "Наличные",
    3: "Cash"
}

BTN_PAY_CARD = {
    1: "Karta",
    2: "Карта",
    3: "Card"
}

BTNS_PAYMENT = {
    1: [
        [KeyboardButton(text="Naqd pul"), KeyboardButton(text="Karta")],
        [KeyboardButton(text="Orqaga")]
    ],
    2: [
        [KeyboardButton(text="Наличные"), KeyboardButton(text="Карта")],
        [KeyboardButton(text="Назад")]
    ],
    3: [
        [KeyboardButton(text="Cash"), KeyboardButton(text="Card")],
        [KeyboardButton(text="Back")]
    ]
}

BTNS_PAYMENT_INLINE = {
    1: [
        [InlineKeyboardButton(text="Naqd pul", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Karta", callback_data="order_payment_2")]
    ],
    2: [
        [InlineKeyboardButton(text="Наличные", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Карта", callback_data="order_payment_2")]
    ],
    3: [
        [InlineKeyboardButton(text="Cash", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Card", callback_data="order_payment_2")]
    ]
}

BTNS_PAYMENT_INLINE_RU = {
    1: [
        [InlineKeyboardButton(text="Naqd pul", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Karta", callback_data="order_payment_2")]
    ],
    2: [
        [InlineKeyboardButton(text="Наличные", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Карта", callback_data="order_payment_2")]
    ],
    3: [
        [InlineKeyboardButton(text="Cash", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Card", callback_data="order_payment_2")]
    ]
}

BTNS_PAYMENT_INLINE_ENG = {
    1: [
        [InlineKeyboardButton(text="Naqd pul", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Karta", callback_data="order_payment_2")]
    ],
    2: [
        [InlineKeyboardButton(text="Наличные", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Карта", callback_data="order_payment_2")]
    ],
    3: [
        [InlineKeyboardButton(text="Cash", callback_data="order_payment_1")],
        [InlineKeyboardButton(text="Card", callback_data="order_payment_2")]
    ]
}

PAYMENT_METHOD_TEXT = {
    1: "Naqd pul",  # For order summary
    2: "Karta"
}

PAYMENT_METHOD_TEXT_RU = {
    1: "Наличные",
    2: "Карта"
}

PAYMENT_METHOD_TEXT_ENG = {
    1: "Cash",
    2: "Card"
}

PAYMENT_METHOD_FULL = {
    1: {"uz": "Naqd pul", "ru": "Наличные", "eng": "Cash"},
    2: {"uz": "Karta", "ru": "Карта", "eng": "Card"}
}












PAYMENT_TEXT = {
    'cash': {
        1: "Naqd pul",
        2: "Наличные",
        3: "Cash"
    },
    'card': {
        1: "Karta",
        2: "Карта",
        3: "Card"
    }
}

TEXT_PAYMENT_CHOICE = {
    1: "💰 To'lov usulini tanlang:",
    2: "💰 Выберите способ оплаты:",
    3: "💰 Choose payment method:"
}
