#!/usr/bin/env python3
"""Fix hardcoded image path in inlines.py"""

file_path = "/app/tgbot/tgb/inlines.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace the hardcoded image path section (lines 115-127)
new_code = """                # Send product image if available
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
                            text=f"{caption}\\n\\n⚠️ Rasm yuklanmadi",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                        )
                else:
                    logger.warning(f"⚠️ NO IMAGE: Product {data_sp[2]} has no image in database")
                    query.message.reply_text(
                        text=f"{caption}\\n\\n📷 Rasm mavjud emas",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                    )
"""

# Replace lines 115-127 (index 114-126)
if len(lines) > 127:
    # Check if it's the hardcoded path
    if 'image_path = f"/app/media/products/main/product_' in lines[115]:
        lines[115:127] = [new_code]
        print("✅ Fixed hardcoded image path in inlines.py")
    else:
        print("⚠️ Warning: Line 115 doesn't contain expected hardcoded path")
        print(f"Line 115: {lines[115][:80]}")
else:
    print("❌ Error: File doesn't have enough lines")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("📝 File updated successfully!")
