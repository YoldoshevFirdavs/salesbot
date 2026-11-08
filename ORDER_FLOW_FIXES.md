# Buyurtma Berish Jarayonini To'g'rilash

## Muammolar:
1. ✅ Telefon raqam o'rniga ism ko'rinadi
2. ✅ Buyurtmalarimni ko'rish ishlamayapti
3. ✅ Buyurtma jarayoni to'liq emas
4. ✅ Mahsulotlar admin ga yuborilmayapti

---

## 1. Telefon Raqam Muammosi

**Muammo:** Admin ga xabar yuborishda telefon raqam o'rniga ism chiqmoqda.

**Sabab:** `runbot.py` da `db_user['phone_number']` o'rniga `db_user['full_name']` ishlatilgan.

**Yechim:**

```python
# runbot.py - location_handler funksiyasida
context.bot.send_message(
    chat_id=ADMIN_ID,
    text=f"<b>Yangi buyurtma:</b>\n\n"
         f"👤 <b>Ism-familiya:</b> {db_user.get('full_name', 'Noma\'lum')}\n"
         f"📞 <b>Telefon raqam:</b> {db_user.get('phone_number', 'Noma\'lum')} \n\n"  # Bu qator to'g'ri
         f"💳 <b>To'lov:</b> {'Naqd pul' if payment_method == 'cash' else 'Karta'}\n"
         f"📥 <b>Buyurtma:</b> \n"
         f"{text}",
    parse_mode='HTML'
)
```

---

## 2. Buyurtmalarimni Ko'rish

**Muammo:** "Mening buyurtmalarim" tugmasi ishlamayapti.

**Yechim:**

`messages.py` faylida `TEXT_MY_ORDERS` tugmasi uchun handler qo'shish kerak:

```python
# messages.py ichida
elif message_text == globals.TEXT_MY_ORDERS[db_user['language']]:
    # Get user's active orders
    orders = db.get_user_orders(db_user['id'])
    
    if not orders:
        update.message.reply_text(
            text="❌ Sizda faol buyurtmalar yo'q",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
    else:
        text = "📦 <b>Sizning buyurtmalaringiz:</b>\n\n"
        for order in orders:
            text += f"🆔 Buyurtma #{order.id}\n"
            text += f"💰 Summa: {order.total_price} so'm\n"
            text += f"📅 Sana: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            text += f"📊 Holat: {order.get_status_display()}\n"
            text += "---\n\n"
        
        update.message.reply_text(
            text=text,
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
```

---

## 3. To'liq Buyurtma Jarayoni

### A. Mahsulot Tanlash ✅ (Ishlayapti)
- Category → Product → Miqdor tanlash

### B. Savatcha Ko'rish ✅ (Ishlayapti)
- Savatchani ko'rish
- Mahsulotlar ro'yxati

### C. Buyurtma Berish (TO'G'RILASH KERAK)

**1-qadam:** To'lov usulini tanlash
```python
# inlines.py - cart handler
elif data_sp[0] == "cart":
    if len(data_sp) == 1:  # cart tugmasi bosilganda
        carts = context.user_data.get("carts", {})
        if not carts:
            query.message.edit_text(
                text="❌ Savatingiz bo'sh",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cart_back")]
                ])
            )
            return
        
        # Savatcha ma'lumotlarini ko'rsatish
        text = f"🛒 <b>Savatingiz:</b>\n\n"
        lang_code = globals.LANGUAGE_CODE[db_user['language']]
        total_price = 0
        
        for cart_id, quantity in carts.items():
            product = db.get_product_for_cart(int(cart_id))
            if product:
                text += f"{quantity} x {product[f'name_{lang_code}']}\n"
                text += f"   {product['price']} so'm x {quantity} = {product['price'] * quantity} so'm\n\n"
                total_price += product['price'] * quantity
        
        text += f"💰 <b>Jami:</b> {total_price} so'm"
        
        buttons = [
            [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="order")],
            [InlineKeyboardButton(text="🗑 Savatchani tozalash", callback_data="cart_clear")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cart_back")],
        ]
        
        query.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
            parse_mode='HTML'
        )
```

**2-qadam:** Location yuborish
```python
# inlines.py - order handler
elif data_sp[0] == "order":
    if len(data_sp) > 1 and data_sp[1] == "payment":
        # To'lov usuli tanlandi
        context.user_data['payment_type'] = int(data_sp[2])
        query.message.delete()
        query.message.reply_text(
            text="📍 Yetkazib berish manzilini yuboring:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="📍 Lokatsiya yuborish", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    else:
        # To'lov usulini tanlash
        buttons = [
            [InlineKeyboardButton(text="💵 Naqd pul", callback_data="order_payment_1")],
            [InlineKeyboardButton(text="💳 Karta", callback_data="order_payment_2")],
        ]
        query.message.edit_text(
            text="💳 To'lov usulini tanlang:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
```

**3-qadam:** Buyurtmani saqlash va adminга yuborish
```python
# runbot.py - location_handler
def location_handler(update, context):
    db_user = db.get_user_by_chat_id(update.message.from_user.id)
    location = update.message.location
    payment_type = context.user_data.get("payment_type", 1)
    
    # Address
    address = f"Lat: {location.latitude}, Lon: {location.longitude}"
    
    # Phone number
    phone_number = db_user.get('phone_number', '')
    
    # Payment method
    payment_method = "cash" if payment_type == 1 else "card"
    
    # Create order
    db.create_order(db_user['id'], context.user_data.get("carts", {}), payment_method, address, phone_number)
    
    # Prepare order text for admin
    text = ""
    total_price = 0
    
    if context.user_data.get("carts", {}):
        carts = context.user_data.get("carts")
        lang_code = globals.LANGUAGE_CODE.get(db_user['language'], 'uz')
        
        for cart_id, quantity in carts.items():
            product = db.get_product_for_cart(int(cart_id))
            if product:
                text += f"{quantity} x {product[f'name_{lang_code}']} - {product['price'] * quantity} so'm\n"
                total_price += product['price'] * quantity
        
        text += f"\n💰 Jami: {total_price} so'm"
    
    # Send to admin
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"<b>🔔 YANGI BUYURTMA!</b>\n\n"
             f"👤 <b>Mijoz:</b> {db_user.get('full_name', 'Noma\\'lum')}\n"
             f"📞 <b>Telefon:</b> {db_user.get('phone_number', 'Noma\\'lum')}\n"
             f"💳 <b>To\\'lov:</b> {'💵 Naqd pul' if payment_method == 'cash' else '💳 Karta'}\n\n"
             f"📦 <b>Mahsulotlar:</b>\n"
             f"{text}",
        parse_mode='HTML'
    )
    
    # Send location to admin
    context.bot.send_location(
        chat_id=ADMIN_ID,
        latitude=float(location.latitude),
        longitude=float(location.longitude)
    )
    
    # Clear cart
    context.user_data.pop("carts", None)
    context.user_data.pop("payment_type", None)
    
    # Send success message to user
    update.message.reply_text(
        text="✅ Buyurtmangiz qabul qilindi!\n\n"
             "Tez orada operator siz bilan bog'lanadi.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🛒 Buyurtma berish")],
                [KeyboardButton(text="📦 Mening buyurtmalarim"), KeyboardButton(text="ℹ️ Biz haqimizda")],
                [KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="❓ Yordam")]
            ],
            resize_keyboard=True
        )
    )
```

---

## 4. ADMIN_ID ni To'g'rilash

`.env` faylida ADMIN_ID ni tekshiring:

```env
ADMIN_ID=your_telegram_user_id
```

Admin ID ni topish uchun:
1. Telegram botda /start bosing
2. Loglarni ko'ring: `docker logs salesbot-tgbot-1 | grep "chat_id"`
3. Sizning chat_id ni ko'rishingiz mumkin

---

## 5. Buyurtmalar Statuslarini Ko'rsatish

Order modelida status choices bor, ularni to'g'ri ko'rsatish kerak:

```python
# models.py ichida
class OrderStatus(models.TextChoices):
    PENDING = "Pending", "⏳ Kutilmoqda"
    PROCESSING = "Processing", "🔄 Tayyorlanmoqda"
    READY_FOR_DELIVERY = "Ready for Delivery", "📦 Yetkazishga tayyor"
    DELIVERED = "Delivered", "✅ Yetkazildi"
    CANCELED = "Canceled", "❌ Bekor qilindi"
```

---

## Qo'shimcha Tavsiyalar

### 1. Savatchani Tozalash
Buyurtma muvaffaqiyatli yaratilgandan keyin savatchani tozalash:
```python
context.user_data.pop("carts", None)
context.user_data.pop("payment_type", None)
```

### 2. Xatoliklarni Boshqarish
```python
try:
    db.create_order(...)
except Exception as e:
    logger.error(f"Error creating order: {e}")
    update.message.reply_text("❌ Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.")
    return
```

### 3. Buyurtma Tarixini Ko'rish
```python
# messages.py
elif message_text == "📦 Mening buyurtmalarim":
    orders = db.get_user_orders(db_user['id'])
    # Ko'rsatish...
```

---

## Testlash Tartibi

1. ✅ /start - Bot ishga tushishi
2. ✅ 🛒 Buyurtma berish - Kategoriyalar chiqishi
3. ✅ Kategoriya tanlash - Mahsulotlar chiqishi  
4. ✅ Mahsulot tanlash - Rasm + 1-9 tugmalar
5. ✅ Miqdor tanlash - Savatchaga qo'shilishi
6. ✅ 🛒 Savatcha - Mahsulotlar ko'rinishi
7. ✅ ✅ Buyurtma berish - To'lov tanlash
8. ✅ 💵 Naqd/Karta - Location so'rashi
9. ✅ 📍 Location yuborish - Admin ga xabar + Muvaffaqiyatli xabar
10. ✅ 📦 Buyurtmalarim - Buyurtmalar ro'yxati

---

## Kerakli O'zgarishlar Ro'yxati

### Fayl: `tgbot/tgb/runbot.py`
- ✅ `location_handler` da telefon raqam to'g'rilash
- ✅ Admin ga yuborilayotgan xabar formatini yaxshilash
- ✅ Savatchani tozalash qo'shish

### Fayl: `tgbot/tgb/messages.py`  
- ⚠️ "Mening buyurtmalarim" uchun handler qo'shish

### Fayl: `tgbot/tgb/inlines.py`
- ✅ Savatchani ko'rsatish formatini yaxshilash
- ✅ To'lov tanlash xabarini yaxshilash

### Fayl: `.env`
- ⚠️ ADMIN_ID ni to'g'ri o'rnatish

---

## Har bir muammoni hal qilish buyruqlari

Men har bir muammoni alohida tuzataman. Quyidagi ketma-ketlikda ishlang:

1. Telefon raqam to'g'rilash ✅
2. Admin xabar formatini yaxshilash ✅
3. Savatchani tozalash qo'shish ✅
4. "Buyurtmalarim" handler qo'shish ⚠️
5. ADMIN_ID tekshirish ⚠️

Tayyor bo'lsangiz, har birini ketma-ket tuzatayman!
