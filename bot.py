from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK8"
CONTACT = "@DINOS76S"

# ---------------------- PRODUITS ----------------------
products_choco = {
    "frozen": {
        "name": "🥶 FROZEN SIFT",
        "desc": "Garlic Cookie 🍪\nJelly Donuts 🍩\nCake 🍰\nPromo -25%",
        "video": "caliplates.mp4",
        "prices": ["2,5G 50€", "5G 90€", "10G 180€", "20G 350€", "25G 400€"]
    },
    "gaz": {
        "name": "⚡️ Gaz fruit 90u",
        "desc": "Papaya Dolce 🥭\nMimi Cheese 🧀",
        "video": "gaz.mp4",
        "prices": ["10G 130€", "25G 240€", "50G 450€"]
    },
    "calimountain": {
        "name": "🧑‍🌾 CALIMOUNTAIN 120u",
        "desc": "Candy Gaz 🍬\nGlitter Bomb 💣\nApple Mintz 🍏",
        "video": "120u.mp4",
        "prices": ["5G 70€", "10G 140€", "20G 260€", "25G 310€"]
    },
    "farm": {
        "name": "🥶 FRESH FROZEN SIFT",
        "desc": "PERMANENT MAKER x GELATO 41 ⛽️🍦",
        "video": "farm.mp4",
        "prices": ["5G 70€", "10G 140€", "20G 250€", "25G 300€"]
    }
}

cali = {
    "name": "🇺🇸 Cali weed",
    "desc": "Runtz 🌈\nTropicana Strawberry 🌴🍓",
    "video": "cali.mp4",
    "prices": ["3G 40€", "5G 60€", "10G 120€", "20G 230€", "25G 300€"]
}

# ---------------------- UTIL ----------------------
async def delete_current_message(message):
    try:
        await message.delete()
    except:
        pass

# ---------------------- START ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await delete_current_message(query.message)
        message = query.message
    else:
        message = update.message

    keyboard = [
        [InlineKeyboardButton("Menu📝", callback_data="menu")],
        [
            InlineKeyboardButton("Info ℹ️ livraison 🚚", callback_data="info_livraison"),
            InlineKeyboardButton("Info ℹ️ Meet-up 📍", callback_data="info_meetup")
        ],
        [
            InlineKeyboardButton("Instagram 📸", url="https://www.instagram.com/dinoterps76?igsh=b3ZjMGo4dGMxc2tz&utm_source=qr"),
            InlineKeyboardButton("Patato 🥔", url="https://duanym138.org/DINOfslmogx8")
        ],
        [
            InlineKeyboardButton("Canal Telegram", url="https://t.me/+j7EMkLSIaV83ZmU8"),
            InlineKeyboardButton("Snapchat 👻", url="https://snapchat.com/t/EZAiDCkN")
        ]
    ]

    await message.reply_photo(
        photo=open("dino.jpg", "rb"),
        caption=(
            "SALUT A TOUS LA TEAM BIENVENUE CHEZ NOUS L’EQUIPE 🔥🦾\n\n"
            "DINO TERPS 76\n"
            "🍓🍒🍋🍊🍈\n\n"
            "The best of terps au rendez vous des produits exceptionnels\n"
            "Prix imbattable dans toute la Normandie 🏆\n\n"
            "Livraison 🚚 ✅\n"
            "76 / 27 / 14 / 60\n\n"
            "Meet-Up 🏠 76 ✅\n\n"
            "Contact unique :\n"
            "@dino76s 🍣\n\n"
            "Toute ce passe ci-dessous 👇👇"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------------- INFO LIVRAISON ----------------------
async def info_livraison(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    await query.message.reply_text(
        "SALUT A TOUS LA TEAM !\n\n"
        "VOICI LES ZONES DE LIVRAISON 🚚 📦\n"
        "76 / 27 / 14 / 60\n\n"
        "76 centre et alentours\n\n"
        "- 10 km : 50€\n"
        "- 20 km : 80€\n"
        "- 30 km : 120€\n"
        "- 50 km : 350€\n"
        "- 100 km : 420€\n\n"
        "Paiement en espèce 💶\n\n"
        "Contact : @dinos76s 🍱",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ Retour", callback_data="start")]]
        )
    )

# ---------------------- INFO MEET-UP ----------------------
async def info_meetup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    await query.message.reply_text(
        "SERVICE MEET-UP 🏠\n\n"
        "Passe directement sur place\n"
        "Contacte en privé avant avec l’heure et la commande\n\n"
        "@dino76s 🍣\n\n"
        "Paiement en espèce 💶\n\n"
        "Ouvert 12h - 23h\n"
        "SAV 24h/24",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ Retour", callback_data="start")]]
        )
    )

# ---------------------- MENUS ----------------------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    keyboard = [
        [InlineKeyboardButton("🍫", callback_data="choco")],
        [InlineKeyboardButton("🌳", callback_data="tree")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="start")]
    ]
    await query.message.reply_text(
        "Menu",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def choco_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    keyboard = [[InlineKeyboardButton(p["name"], callback_data=f"prod_{k}")] for k, p in products_choco.items()]
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="menu")])

    await query.message.reply_text(
        "Produits",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def cali_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    keyboard = [
        [InlineKeyboardButton(cali["name"], callback_data="cali_detail")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="menu")]
    ]
    await query.message.reply_text(
        "Cali weed",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    key = query.data.replace("prod_", "")
    p = products_choco[key]

    caption = f"{p['name']}\n\n{p['desc']}\n\nTarifs :\n" + "\n".join(p["prices"])

    keyboard = [
        [InlineKeyboardButton("📩 Contact", url=f"https://t.me/{CONTACT.replace('@','')}")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="choco")]
    ]

    await query.message.reply_video(
        video=open(p["video"], "rb"),
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def cali_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await delete_current_message(query.message)

    caption = f"{cali['name']}\n\n{cali['desc']}\n\nTarifs :\n" + "\n".join(cali["prices"])

    keyboard = [
        [InlineKeyboardButton("📩 Contact", url=f"https://t.me/{CONTACT.replace('@','')}")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="tree")]
    ]

    await query.message.reply_video(
        video=open(cali["video"], "rb"),
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------------- MAIN ----------------------
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(start, pattern="start"))
app.add_handler(CallbackQueryHandler(menu, pattern="menu"))
app.add_handler(CallbackQueryHandler(choco_menu, pattern="choco"))
app.add_handler(CallbackQueryHandler(cali_menu, pattern="tree"))
app.add_handler(CallbackQueryHandler(product_detail, pattern="prod_"))
app.add_handler(CallbackQueryHandler(cali_detail, pattern="cali_detail"))
app.add_handler(CallbackQueryHandler(info_livraison, pattern="info_livraison"))
app.add_handler(CallbackQueryHandler(info_meetup, pattern="info_meetup"))

app.run_polling()
