from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK8"
CONTACT = "@DINOS76S"

# ---------- PRODUITS ----------
products_choco = {
    "frozen": {
        "name": "🥶 FROZEN SIFT",
        "desc": "Garlic Cookie 🍪, Jelly Donuts 🍩, Cake 🍰\nPromo -25%",
        "video": "videos/frozen.mp4",
        "prices": ["2,5G 50€", "5G 90€", "10G 180€", "20G 350€", "25G 400€"]
    },
    "gaz": {
        "name": "⚡️ Gaz fruit 90u",
        "desc": "Papaya Dolce 🥭, Mimi Cheese 🧀",
        "video": "videos/gaz.mp4",
        "prices": ["10G 130€", "25G 240€", "50G 450€"]
    },
    "calimountain": {
        "name": "🧑‍🌾 CALIMOUNTAIN 120u",
        "desc": "Candy Gaz 🍬, Glitter Bomb 💣, Apple Mintz 🍏",
        "video": "videos/calimountain.mp4",
        "prices": ["5G 70€", "10G 140€", "20G 260€", "25G 310€"]
    },
    "farm": {
        "name": "🥶 FRESH FROZEN SIF",
        "desc": "PERMANENT MAKER x GELATO 41 ⛽️🍦",
        "video": "videos/farm.mp4",
        "prices": ["5G 70€", "10G 140€", "20G 250€", "25G 300€"]
    }
}

cali = {
    "name": "🇺🇸 Cali weed",
    "desc": "Runtz 🌈, Tropicana Strawberry 🌴🍓",
    "video": "videos/cali.mp4",
    "prices": ["3G 40€", "5G 60€", "10G 120€", "20G 230€", "25G 300€"]
}

# ---------- COMMANDES ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Menu📝", callback_data="menu")]]
    
    # Envoi image + texte + bouton
    await update.message.reply_photo(
        photo=open("dino.jpg", "rb"),
        caption="🦖🍣 *Bienvenue sur DINO TERPS 76*\nAppuie sur les boutons ci-dessous pour voir le menu",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🍫", callback_data="choco")],
        [InlineKeyboardButton("🌳", callback_data="tree")]
    ]
    await query.edit_message_text(
        "📋 *Menu📝*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def choco_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(p["name"], callback_data=f"prod_{k}")] for k, p in products_choco.items()]
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="menu")])
    await query.edit_message_text(
        "🍫 *Produits*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def cali_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(cali["name"], callback_data="cali_detail")],
        [InlineKeyboardButton("📩 Contact", url=f"https://t.me/{CONTACT.replace('@','')}")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="menu")]
    ]
    await query.edit_message_text(
        "🌳 *Cali weed*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.replace("prod_", "")
    p = products_choco[key]

    # Préparer texte avec prix
    prices_text = "\n".join(p["prices"])
    caption = f"*{p['name']}*\n\n{p['desc']}\n\n💰 *Tarifs*\n{prices_text}"

    # Envoie la vidéo avec caption + boutons
    await query.message.reply_video(
        video=open(p["video"], "rb"),
        caption=caption,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Contact", url=f"https://t.me/{CONTACT.replace('@','')}")],
            [InlineKeyboardButton("⬅️ Retour", callback_data="choco")]
        ])
    )

async def cali_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prices_text = "\n".join(cali["prices"])
    caption = f"*{cali['name']}*\n\n{cali['desc']}\n\n💰 *Tarifs*\n{prices_text}"

    await query.message.reply_video(
        video=open(cali["video"], "rb"),
        caption=caption,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Contact", url=f"https://t.me/{CONTACT.replace('@','')}")],
            [InlineKeyboardButton("⬅️ Retour", callback_data="tree")]
        ])
    )

# ---------- MAIN ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(menu, pattern="menu"))
app.add_handler(CallbackQueryHandler(choco_menu, pattern="choco"))
app.add_handler(CallbackQueryHandler(cali_menu, pattern="tree"))
app.add_handler(CallbackQueryHandler(product_detail, pattern="prod_"))
app.add_handler(CallbackQueryHandler(cali_detail, pattern="cali_detail"))

app.run_polling()
