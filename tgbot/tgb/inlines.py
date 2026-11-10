import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from database import Database
import bot_globals as globals
import bot_methods
from tgbot.tgb.logger import logger

db = Database()

def inline_handler(update, context):
    query = update.callback_query
    data_sp = str(query.data).split("_")
    db_user = db.get_user_by_chat_id(query.message.chat_id)
    
    # Null check for db_user
    if not db_user:
        query.message.reply_text("Iltimos, avval /start buyrug'ini bosing.")
        return

    if data_sp[0] == "category":
        if data_sp[1] == "product":
            if data_sp[2] == "back":
                # Back to parent category or main menu
                query.message.delete()
                if len(data_sp) > 3:
                    products = db.get_products_by_category(category_id=int(data_sp[3]))
                    buttons = bot_methods.send_product_buttons(products=products, lang_id=db_user["language"])
                else:
                    categories = db.get_categories_by_parent()
                    buttons = bot_methods.send_category_buttons(categories=categories, lang_id=db_user["language"])
                
                clicked_btn = db.get_category_parent(int(data_sp[3])) if len(data_sp) > 3 else None

                if clicked_btn and clicked_btn.get('parent_id'):
                    buttons.append([InlineKeyboardButton(
                        text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"
                    )])
                else:
                    buttons.append([InlineKeyboardButton(
                        text="Back", callback_data="category_back"
                    )])

                query.message.reply_text(
                    text=globals.TEXT_ORDER[db_user['language']],
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif len(data_sp) == 4:
                # Add to cart
                query.message.delete()
                carts = context.user_data.get("carts", {})
                try:
                    quantity = int(data_sp[3])
                    product = db.get_product_by_id(int(data_sp[2]))
                    if product['stock'] < quantity:
                        query.message.reply_text("Yetarli zaxira yo'q!")
                        return
                    carts[f"{data_sp[2]}"] = carts.get(f"{data_sp[2]}", 0) + quantity
                except ValueError:
                    logger.error(f"Invalid quantity: {data_sp[3]}")
                context.user_data["carts"] = carts
                logger.info(f"🛒 CART: User {db_user['chat_id']} added product {data_sp[2]} to cart, quantity: {data_sp[3]}")

                categories = db.get_categories_by_parent()
                buttons = bot_methods.send_category_buttons(categories=categories, lang_id=db_user["language"])

                text = f"{globals.AT_KORZINKA[db_user['language']]}:\n\n"
                lang_code = globals.LANGUAGE_CODE[db_user['language']]
                total_price = 0
                for cart, val in carts.items():
                    product = db.get_product_for_cart(int(cart))
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
                    total_price += product['price'] * val

                text += f"\n{globals.ALL[db_user['language']]}: {total_price}"
                buttons.append([InlineKeyboardButton(text=f"{globals.BTN_KORZINKA[db_user['language']]}",
                                                     callback_data="cart")])

                query.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )

            else:
                # View product details
                product = db.get_product_by_id(int(data_sp[2]))
                if not product:
                    query.message.delete()
                    query.message.reply_text("Mahsulot topilmadi!")
                    return
                    
                query.message.delete()
                logger.info(f"📦 PRODUCT: User {db_user['chat_id']} viewed product {data_sp[2]}")

                lang_code = globals.LANGUAGE_CODE[db_user['language']]
                caption = f"{globals.TEXT_PRODUCT_PRICE[db_user['language']]} {product['price']}\n{globals.TEXT_PRODUCT_DESC[db_user['language']]} {product[f'description_{lang_code}']}"

                buttons = [
                    [
                        InlineKeyboardButton(text="1️⃣", callback_data=f"category_product_{data_sp[2]}_1"),
                        InlineKeyboardButton(text="2️⃣", callback_data=f"category_product_{data_sp[2]}_2"),
                        InlineKeyboardButton(text="3️⃣", callback_data=f"category_product_{data_sp[2]}_3"),
                    ],
                    [
                        InlineKeyboardButton(text="4️⃣", callback_data=f"category_product_{data_sp[2]}_4"),
                        InlineKeyboardButton(text="5️⃣", callback_data=f"category_product_{data_sp[2]}_5"),
                        InlineKeyboardButton(text="6️⃣", callback_data=f"category_product_{data_sp[2]}_6"),
                    ],
                    [
                        InlineKeyboardButton(text="7️⃣", callback_data=f"category_product_{data_sp[2]}_7"),
                        InlineKeyboardButton(text="8️⃣", callback_data=f"category_product_{data_sp[2]}_8"),
                        InlineKeyboardButton(text="9️⃣", callback_data=f"category_product_{data_sp[2]}_9"),
                    ],
                    [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"category_product_back_{product['category_id']}")],
                ]

                # Send product image if available
                if product.get('image'):
                    try:
                        query.message.reply_photo(
                            photo=open(product['image'], 'rb'),
                            caption=caption,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                        )
                        logger.info(f"📷 IMAGE: Sent product {data_sp[2]} image from database path: {product['image']}")
                    except Exception as e:
                        logger.error(f"❌ IMAGE ERROR: Could not send image for product {data_sp[2]}: {e}")
                        query.message.reply_text(
                            text=f"{caption}\n\n⚠️ Rasm yuklanmadi",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                        )
                else:
                    logger.warning(f"⚠️ NO IMAGE: Product {data_sp[2]} has no image in database")
                    query.message.reply_text(
                        text=f"{caption}\n\n📷 Rasm mavjud emas",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                    )
        
        elif data_sp[1] == "back":
            # Back to parent category
            parent_id = int(data_sp[2]) if len(data_sp) > 2 else None
            categories = db.get_categories_by_parent(parent_id=parent_id)
            buttons = bot_methods.send_category_buttons(categories=categories, lang_id=db_user["language"])

            if parent_id:
                clicked_btn = db.get_category_parent(parent_id)
                if clicked_btn and clicked_btn.get('parent_id'):
                    buttons.append([InlineKeyboardButton(
                        text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"
                    )])
                else:
                    buttons.append([InlineKeyboardButton(text="Back", callback_data="category_back")])

            query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        else:
            # View category (check if it has children or products)
            category_id = int(data_sp[1])
            children = db.get_categories_by_parent(parent_id=category_id)
            
            if children:
                # Has child categories
                buttons = bot_methods.send_category_buttons(categories=children, lang_id=db_user["language"])
                clicked_btn = db.get_category_parent(category_id)
                if clicked_btn and clicked_btn.get('parent_id'):
                    buttons.append([InlineKeyboardButton(
                        text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"
                    )])
                else:
                    buttons.append([InlineKeyboardButton(text="Back", callback_data="category_back")])
                query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            else:
                # Has products
                products = db.get_products_by_category(category_id=category_id)
                buttons = bot_methods.send_product_buttons(products=products, lang_id=db_user["language"])
                clicked_btn = db.get_category_parent(category_id)
                if clicked_btn and clicked_btn.get('parent_id'):
                    buttons.append([InlineKeyboardButton(
                        text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"
                    )])
                else:
                    buttons.append([InlineKeyboardButton(text="Back", callback_data="category_back")])
                query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    
    elif data_sp[0] == "cart":
        if len(data_sp) == 2 and data_sp[1] == "clear":
            context.user_data.pop("carts", None)
            categories = db.get_categories_by_parent()
            buttons = bot_methods.send_category_buttons(categories=categories, lang_id=db_user["language"])
            query.message.edit_text(text=globals.TEXT_ORDER[db_user['language']], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        elif len(data_sp) == 2 and data_sp[1] == "back":
            categories = db.get_categories_by_parent()
            buttons = bot_methods.send_category_buttons(categories=categories, lang_id=db_user["language"])
            
            if context.user_data.get("carts", {}):
                carts = context.user_data.get("carts")
                text = f"{globals.AT_KORZINKA[db_user['language']]}:\n\n"
                lang_code = globals.LANGUAGE_CODE[db_user['language']]
                total_price = 0
                for cart, val in carts.items():
                    product = db.get_product_for_cart(int(cart))
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
                    total_price += product['price'] * val
                text += f"\n{globals.ALL[db_user['language']]}: {total_price}"
                buttons.append([InlineKeyboardButton(text=globals.BTN_KORZINKA[db_user['language']], callback_data="cart")])
            else:
                text = globals.TEXT_ORDER[db_user['language']]
            query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        else:
            # Show cart with order button
            carts = context.user_data.get("carts", {})
            if not carts:
                query.message.edit_text(
                    text="❌ Savatingiz bo'sh",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cart_back")]
                    ])
                )
                return
            
            # Show cart items
            text = "🛒 <b>Savatingiz:</b>\n\n"
            lang_code = globals.LANGUAGE_CODE.get(db_user['language'], 'uz')
            total_price = 0
            
            for cart_id, quantity in carts.items():
                product = db.get_product_for_cart(int(cart_id))
                if product:
                    item_price = product['price'] * quantity
                    product_name = product.get(f'name_{lang_code}', 'Product')
                    text += "{} x {} - {:,.0f} so'm\n".format(quantity, product_name, item_price)
                    total_price += item_price
            
            text += "\n💰 <b>Jami:</b> {:,.0f} so'm".format(total_price)
            
            buttons = [
                [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="order")],
                [InlineKeyboardButton(text="🗑 Savatchani bo'shatish", callback_data="cart_clear")],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cart_back")],
            ]
            query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode='HTML')
    
    elif data_sp[0] == "order":
        if len(data_sp) > 1 and data_sp[1] == "payment":
            payment_method = int(data_sp[2])  # 1 = cash, 2 = card
            context.user_data['payment_method'] = payment_method
            query.message.delete()
            
            if payment_method == 2:  # Card payment - show Stripe checkout link
                # Get user's orders to find the most recent one
                carts = context.user_data.get("carts", {})
                if carts:
                    from order_utils import create_order_from_cart
                    order_id = create_order_from_cart(db_user['chat_id'], db_user, carts, payment_method)
                    
                    if order_id:
                        checkout_url = f"{os.getenv('API_BASE_URL')}/checkout/{order_id}/"
                        query.message.reply_text(
                            text=(
                                f"💳 <b>Karta to'lovini amalga oshiring</b>\n\n"
                                f"Pastdagi linkga bosib, to'lov ma'lumotlarini kiriting:\n\n"
                                f"<a href='{checkout_url}'>💳 To'lovni amalga oshirish</a>\n\n"
                                f"To'lov muvaffaqiyatli bo'lgandan keyin avtomatik ravishda qayta Telegramga qaytarsiz."
                            ),
                            parse_mode='HTML',
                            disable_web_page_preview=False
                        )
                        logger.info(f"💳 PAYMENT LINK: User {db_user['chat_id']} sent Stripe checkout link for order {order_id}")
                    else:
                        query.message.reply_text("❌ Buyurtma yaratishda xatolik yuz berdi")
            else:  # Cash payment
                query.message.reply_text(
                    text=globals.BTN_SEND_LOCATION[db_user["language"]],
                    reply_markup=ReplyKeyboardMarkup(
                        [[KeyboardButton(text=globals.BTN_SEND_LOCATION[db_user["language"]], request_location=True)]],
                        resize_keyboard=True
                    )
                )
        else:
            buttons = [
                [
                    InlineKeyboardButton(text=f"💵 {globals.PAYMENT_TEXT['cash'][db_user['language']]}", callback_data="order_payment_1"),
                    InlineKeyboardButton(text=f"💳 {globals.PAYMENT_TEXT['card'][db_user['language']]}", callback_data="order_payment_2"),
                ]
            ]
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
