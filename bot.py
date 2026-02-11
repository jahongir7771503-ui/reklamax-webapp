from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ================== SOZLAMALAR ==================
BOT_TOKEN = "8550090522:AAHBx5gN056eXceZUdZ7-dF2jxZ8N8Tib8g"
OWNER_ID = 98510989  # admin chat id

# ================== STATES ==================
(
    PHONE,
    TYPE,
    ENI,
    BOYI,
    PLACE,
    TEXT_CONTENT,
    AUDIENCE,
    DISTANCE,
    STYLE,
    COLOR,
    GOAL,
    LIGHTING,
    MATERIAL,
    DEADLINE,
    MEDIA,
    CONFIRM,
) = range(16)

# ================== KEYBOARDS ==================
def main_menu_keyboard():
    return ReplyKeyboardMarkup([["🧮 Buyurtma berish"]], resize_keyboard=True)


def phone_keyboard():
    btn = KeyboardButton("📞 Raqamni ulashish", request_contact=True)
    return ReplyKeyboardMarkup([[btn]], resize_keyboard=True, one_time_keyboard=True)


def design_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Banner", "Lightbox"],
            ["Obyom harf", "Prizmatron"],
            ["Ichki reklama", "Boshqa"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def place_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Bino fasadi (tashqi)", "Tom qismi (roof)"],
            ["Ichki interyer (indoor)", "Yo‘l bo‘yi"],
            ["Savdo markazi", "Boshqa"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def audience_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["O‘tib ketayotganlar", "Haydovchilar"],
            ["Savdo markazi mijozlari", "Premium mijozlar"],
            ["Oilaviy auditoriya", "Aralash"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def distance_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["5–10 m", "10–30 m"],
            ["30–50 m", "50 m+"],
            ["Bilmayman"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def style_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Modern (zamonaviy)", "Premium"],
            ["Minimal", "Klassik"],
            ["Yorqin (attention)", "Dizayner tanlasin"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def color_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Qora/Oq", "Qizil"],
            ["Ko‘k", "Sariq"],
            ["Brend ranglari", "Dizayner tanlasin"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def goal_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Uzoqdan ko‘rinsin", "Mijoz jalb qilsin"],
            ["Premium ko‘rinsin", "Brend esda qolsin"],
            ["Sotuvni oshirsin", "Boshqa"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def lighting_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Yoritishsiz", "Ichidan LED"],
            ["Tashqi proyektor", "Tavsiya kerak"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def material_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Akril", "Kompozit (ACP)"],
            ["Banner mato", "PVC/Forex"],
            ["Dizayner tanlasin", "Boshqa"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_keyboard():
    return ReplyKeyboardMarkup(
        [["✅ Tasdiqlash", "🔁 Qayta boshlash"], ["❌ Bekor qilish"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# ================== HELPERS ==================
def clean_text(s: str) -> str:
    return (s or "").strip()


def format_sum(value: int) -> str:
    return f"{value:,}".replace(",", " ") + " so‘m"


def calc_price(eni_cm: float, boyi_cm: float) -> int:
    # NAMUNA formula (keyin real kalkulyator qilamiz)
    m2 = (eni_cm / 100) * (boyi_cm / 100)
    price = int(m2 * 120000)
    return max(price, 50000)


def generate_gpt_prompt(d: dict) -> str:
    # GPT/ChatGPT uchun copy-paste prompt (English)
    return f"""You are a professional outdoor/indoor advertising designer.

Task: Create a realistic, production-ready design concept and layout guidance for a signage project.

Project details:
- Sign type: {d.get("type","-")}
- Size: {d.get("size","-")} (centimeters)
- Installation location: {d.get("place","-")}
- Text/content to include: "{d.get("text_content","-")}"
- Contact/phone (if needed): {d.get("phone","-")}
- Target audience: {d.get("audience","-")}
- Viewing distance: {d.get("distance","-")}
- Style preference: {d.get("style","-")}
- Color preference: {d.get("color","-")}
- Primary goal: {d.get("goal","-")}
- Lighting preference: {d.get("lighting","-")}
- Material preference: {d.get("material","-")}
- Deadline/urgency: {d.get("deadline","-")}

Design requirements (very important):
- Must be readable at the intended viewing distance
- Strong contrast and clear hierarchy (main text vs secondary info)
- Use typography suitable for signage (avoid thin strokes for outdoor)
- Balanced composition (alignment, spacing, margins)
- Consider weather/wind exposure if outdoor; durability and mounting constraints
- If lighting is used, ensure the layout supports night visibility

Output format:
1) 2–3 design concept options (brief but clear)
2) Recommended font direction (e.g., bold geometric sans, condensed, etc.) + why
3) Color palette recommendation with contrast reasoning
4) Layout guidance (text hierarchy, spacing, placement of phone/logo)
5) Lighting recommendation (front-lit/back-lit/halo/none) + why
6) Production notes (thickness/depth, materials, finishing) appropriate for the chosen sign type

Write in a practical, manufacturer-friendly way (not poetic)."""


def customer_thanks_text() -> str:
    return (
        "✅ Buyurtmangiz muvaffaqiyatli qabul qilindi!\n\n"
        "Mutaxassislarimiz siz yuborgan ma’lumotlar asosida "
        "sizga mos **individual reklama dizaynini** qisqa vaqt ichida tayyorlaydi.\n\n"
        "📞 Zarurat bo‘lsa, siz bilan tez orada bog‘lanamiz.\n\n"
        "ReklaMax xizmatini tanlaganingizdan mamnunmiz.\n"
        "Sizga xizmat ko‘rsatish biz uchun sharaf! 🤝"
    )


# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n\n"
        "Siz ReklaMax professional reklama xizmatiga murojaat qildingiz.\n\n"
        "Atigi bir necha savol — va biz sizga mos **eng yaxshi reklama yechimini** tayyorlaymiz.\n\n"
        "Boshlash uchun pastdagi **“Buyurtma berish”** tugmasini bosing. 🧮",
        reply_markup=main_menu_keyboard(),
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❌ Bekor qilindi. Menyu.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END


# ================== FLOW ==================
async def begin_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Buyurtmani boshlashdan oldin siz bilan bog‘lana olishimiz kerak. 📞\n\n"
        "Iltimos, telefon raqamingizni tugma orqali ulashing.",
        reply_markup=phone_keyboard(),
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.contact:
        await update.message.reply_text("Iltimos, raqamni **tugma orqali** ulashing.")
        return PHONE

    context.user_data["phone"] = update.message.contact.phone_number
    await update.message.reply_text(
        "Ajoyib! Endi reklama turini tanlaymiz. 🎯\n\n"
        "Qanday turdagi reklama sizga kerak?",
        reply_markup=design_type_keyboard(),
    )
    return TYPE


async def get_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["type"] = clean_text(update.message.text)
    await update.message.reply_text(
        "Reklama o‘lchamini aniqlaymiz. 📏\n\n"
        "Avvalo **ENI** ni kiriting (sm da).\n"
        "Masalan: 300",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ENI


async def get_eni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = clean_text(update.message.text).replace(",", ".")
    try:
        eni = float(txt)
        if eni <= 0 or eni > 10000:
            raise ValueError
    except Exception:
        await update.message.reply_text("Iltimos, enini faqat raqam bilan kiriting. Masalan: 300")
        return ENI

    context.user_data["eni_cm"] = eni
    await update.message.reply_text(
        "Rahmat! Endi **BO‘YI** ni kiriting (sm da).\nMasalan: 120"
    )
    return BOYI


async def get_boyi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = clean_text(update.message.text).replace(",", ".")
    try:
        boyi = float(txt)
        if boyi <= 0 or boyi > 10000:
            raise ValueError
    except Exception:
        await update.message.reply_text("Iltimos, bo‘yini faqat raqam bilan kiriting. Masalan: 120")
        return BOYI

    context.user_data["boyi_cm"] = boyi
    eni = context.user_data["eni_cm"]
    price = calc_price(eni, boyi)

    context.user_data["price_sum"] = price
    context.user_data["size"] = f"{eni:g} x {boyi:g}"

    await update.message.reply_text(
        "✅ O‘lcham qabul qilindi:\n"
        f"📏 {eni:g} x {boyi:g} sm\n"
        f"💰 Taxminiy narx: {format_sum(price)} "
        "(yakuniy narx dizayn va material tanlangandan so‘ng aniqlanadi)\n\n"
        "Endi reklama qayerga o‘rnatilishini tanlang. 📍",
        reply_markup=place_keyboard(),
    )
    return PLACE


async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["place"] = clean_text(update.message.text)
    await update.message.reply_text(
        "Reklamada aynan qanday yozuv bo‘ladi? ✍️\n\n"
        "Masalan:\n"
        "• “REKLAMAX”\n"
        "• “AKSIYA -50%”\n"
        "• “Ochildi!”",
        reply_markup=ReplyKeyboardRemove(),
    )
    return TEXT_CONTENT


async def get_text_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["text_content"] = clean_text(update.message.text)
    await update.message.reply_text(
        "Bu reklama asosan kimlar uchun? 👥",
        reply_markup=audience_keyboard(),
    )
    return AUDIENCE


async def get_audience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["audience"] = clean_text(update.message.text)
    await update.message.reply_text(
        "Reklama taxminan nechchi metr masofadan ko‘rinishi kerak? 👀",
        reply_markup=distance_keyboard(),
    )
    return DISTANCE


async def get_distance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["distance"] = clean_text(update.message.text)
    await update.message.reply_text("Qaysi dizayn uslubi sizga yaqin? 🎨", reply_markup=style_keyboard())
    return STYLE


async def get_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["style"] = clean_text(update.message.text)
    await update.message.reply_text("Asosiy rang yo‘nalishini tanlang. 🌈", reply_markup=color_keyboard())
    return COLOR


async def get_color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["color"] = clean_text(update.message.text)
    await update.message.reply_text("Reklamaning asosiy vazifasi nima? 🎯", reply_markup=goal_keyboard())
    return GOAL


async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal"] = clean_text(update.message.text)
    await update.message.reply_text("Yoritish bo‘ladimi? 💡", reply_markup=lighting_keyboard())
    return LIGHTING


async def get_lighting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lighting"] = clean_text(update.message.text)
    await update.message.reply_text("Material bo‘yicha xohishingiz bormi? 🧱", reply_markup=material_keyboard())
    return MATERIAL


async def get_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["material"] = clean_text(update.message.text)
    await update.message.reply_text(
        "Buyurtma qachongacha tayyor bo‘lishi kerak? ⏳\n"
        "Masalan: bugun / ertaga / 3 kun / 12-fevralgacha",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEADLINE


async def get_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deadline"] = clean_text(update.message.text)
    await update.message.reply_text(
        "Agar sizda **logo / misol rasm / joyning rasmi** bo‘lsa, shu yerga yuboring. 🖼\n\n"
        "Agar hozircha yo‘q bo‘lsa — `skip` deb yozing.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MEDIA


async def get_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # media optional
    if update.message.photo:
        context.user_data["media"] = ("photo", update.message.photo[-1].file_id)
    elif update.message.document:
        context.user_data["media"] = ("document", update.message.document.file_id)
    else:
        t = clean_text(update.message.text).lower()
        if t == "skip":
            context.user_data["media"] = None
        else:
            await update.message.reply_text("Rasm/fayl yuboring yoki `skip` deb yozing.")
            return MEDIA

    # summary
    eni = context.user_data.get("eni_cm")
    boyi = context.user_data.get("boyi_cm")
    price = context.user_data.get("price_sum")

    summary = (
        "✅ Buyurtma ma’lumotlari tayyor. Tekshirib oling:\n\n"
        f"📌 Turi: {context.user_data.get('type')}\n"
        f"📏 O‘lcham: {eni:g} x {boyi:g} sm\n"
        f"💰 Taxminiy narx: {format_sum(price)} (yakuniy narx keyin aniqlanadi)\n"
        f"📍 Joy: {context.user_data.get('place')}\n"
        f"✍️ Matn: {context.user_data.get('text_content')}\n"
        f"👥 Auditoriya: {context.user_data.get('audience')}\n"
        f"👀 Masofa: {context.user_data.get('distance')}\n"
        f"🎨 Uslub: {context.user_data.get('style')}\n"
        f"🌈 Rang: {context.user_data.get('color')}\n"
        f"🎯 Maqsad: {context.user_data.get('goal')}\n"
        f"💡 Yoritish: {context.user_data.get('lighting')}\n"
        f"🧱 Material: {context.user_data.get('material')}\n"
        f"⏳ Muddat: {context.user_data.get('deadline')}\n\n"
        "Hammasi to‘g‘rimi?"
    )
    await update.message.reply_text(summary, reply_markup=confirm_keyboard())
    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = clean_text(update.message.text).lower()

    if "bekor" in ans or "❌" in ans:
        await update.message.reply_text("❌ Bekor qilindi. Menyu.", reply_markup=main_menu_keyboard())
        context.user_data.clear()
        return ConversationHandler.END

    if "qayta" in ans or "🔁" in ans:
        context.user_data.clear()
        await update.message.reply_text("Mayli, qaytadan boshlaymiz. ✅", reply_markup=main_menu_keyboard())
        return await begin_order(update, context)

    if "tasdiql" in ans or "✅" in ans:
        await send_owner_full(update, context)
        await update.message.reply_text(customer_thanks_text(), reply_markup=main_menu_keyboard())
        context.user_data.clear()
        return ConversationHandler.END

    await update.message.reply_text("Iltimos, ✅ Tasdiqlash / 🔁 Qayta boshlash / ❌ Bekor qilish tanlang.")
    return CONFIRM


# ================== ADMIN SENDING ==================
async def send_owner_full(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    eni = context.user_data.get("eni_cm")
    boyi = context.user_data.get("boyi_cm")
    price = context.user_data.get("price_sum")

    username = f"@{user.username}" if user.username else "(username yo‘q)"

    order_msg = (
        "🆕 YANGI BUYURTMA\n\n"
        f"👤 Mijoz: {user.full_name} {username}\n"
        f"🆔 Chat ID: {chat_id}\n"
        f"📞 Telefon: {context.user_data.get('phone')}\n\n"
        f"📌 Turi: {context.user_data.get('type')}\n"
        f"📏 O‘lcham: {eni:g} x {boyi:g} sm\n"
        f"💰 Taxminiy narx: {format_sum(price)} (yakuniy narx keyin aniqlanadi)\n"
        f"📍 Joy: {context.user_data.get('place')}\n"
        f"✍️ Matn: {context.user_data.get('text_content')}\n"
        f"👥 Auditoriya: {context.user_data.get('audience')}\n"
        f"👀 Masofa: {context.user_data.get('distance')}\n"
        f"🎨 Uslub: {context.user_data.get('style')}\n"
        f"🌈 Rang: {context.user_data.get('color')}\n"
        f"🎯 Maqsad: {context.user_data.get('goal')}\n"
        f"💡 Yoritish: {context.user_data.get('lighting')}\n"
        f"🧱 Material: {context.user_data.get('material')}\n"
        f"⏳ Muddat: {context.user_data.get('deadline')}\n"
    )

    prompt = generate_gpt_prompt(context.user_data)

    await context.bot.send_message(chat_id=OWNER_ID, text=order_msg)
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text="📋 CHATGPT PROMPT (copy-paste)\n\n```text\n" + prompt + "\n```",
    )

    media = context.user_data.get("media")
    if media:
        mtype, fid = media
        if mtype == "photo":
            await context.bot.send_photo(chat_id=OWNER_ID, photo=fid, caption="📎 Mijoz yuborgan rasm/logo")
        else:
            await context.bot.send_document(chat_id=OWNER_ID, document=fid, caption="📎 Mijoz yuborgan fayl/logo")


# ================== APP ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Buyurtma berish"), begin_order)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, get_phone)],
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
            ENI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_eni)],
            BOYI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_boyi)],
            PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_place)],
            TEXT_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text_content)],
            AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_audience)],
            DISTANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_distance)],
            STYLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_style)],
            COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_color)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goal)],
            LIGHTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_lighting)],
            MATERIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_material)],
            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_deadline)],
            MEDIA: [
                MessageHandler(filters.PHOTO, get_media),
                MessageHandler(filters.Document.ALL, get_media),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_media),
            ],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(conv)

    print("🤖 ReklaMax bot ishlayapti...")
    app.run_polling()


if __name__ == "__main__":
    main()
