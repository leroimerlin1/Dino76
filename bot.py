import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# 🔐 METS TON NOUVEAU TOKEN ICI
token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK8"

CHANNEL_ID = -1003733915057
CHANNEL_LINK = "https://t.me/+j7EMkLSIaV83ZmU8"
MINI_APP_URL = "https://leroimerlin1.github.io/Dino76/"
GROUP_LINK = "https://t.me/+mktubkoTrqM0ZjI0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ================================
# Texte Information
# ================================
INFO_TEXT = """🪧 Bienvenue chez DINO TERPS 76 🍱 🪧

NORMANDIE 🇫🇷
✅ QUALITÉ VALIDÉE
🏆 SERVICE NUMÉRO UNO

🌿 DES FRUITS FRAIS 🍇🍊
💎 MEILLEURE QUALITÉ
💰 MEILLEURS PRIX
📦 QUANTITÉ & SATISFACTION GARANTIE ✅

- LIVRAISON •
- MEET UP • 

SERVICE RAPIDE 🚚
🍓 NOTRE ÉQUIPE SE DÉPLACE POUR TOUT LE MONDE ❤️

authenticité, respect et proximité
👉 offrir le meilleur tout en respectant nos prochains 

1 AMIS PARRAINER = -20 SUR COMMANDE🤝 🎁 

Pay*m*nt en Esp*ce 💶 ! 

Ouvert 12h 23h

SAV : 24h 24h ! 🕛
@dino76s"""

# ================================
# Clavier Menu Principal
# ================================
def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("ℹ️ Information", callback_data="info"),
            InlineKeyboardButton("👥 Groupe", url=GROUP_LINK)
        ],
        [
            InlineKeyboardButton("🛍 Boutique", web_app=WebAppInfo(url=MINI_APP_URL))  # Seul sur sa ligne
        ],
        [
            InlineKeyboardButton("📞 Contact", url="https://t.me/dino76s"),
            InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/dinoterps76?igsh=MWlsa2Nkc3lodHVvbg==")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ================================
# Vérification abonnement
# ================================
async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print("Erreur vérification abonnement :", e)
        return False


# ================================
# Commande /start
# ================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return

    is_subscribed = await check_subscription(user.id, context)

    # ❌ PAS ABONNÉ
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("🔔 Rejoindre le canal", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ Vérifier l'abonnement", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🦖 DINO TERPS 76\n\n"
            "🔥 Boutique privée premium\n\n"
            "⚠️ Pour accéder à la Mini App, tu dois rejoindre notre canal officiel.",
            reply_markup=reply_markup
        )
        return

    # ✅ ABONNÉ → Envoi de l'image + menu principal
    with open("dino.jpg", "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption="🍱 Bienvenue chez DINO TERPS 76\n\n🔥 Accès autorisé\n\nChoisis une option ci-dessous 👇",
            reply_markup=main_keyboard()
        )


# ================================
# Gestion des boutons
# ================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check_sub":
        is_subscribed = await check_subscription(query.from_user.id, context)
        if not is_subscribed:
            await query.answer("❌ Tu n'es pas encore abonné.", show_alert=True)
            return

        # Envoi du menu principal avec image
        with open("dino.jpg", "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption="🍱 Accès confirmé !\n\n🔥 Bienvenue dans la boutique exclusive",
                reply_markup=main_keyboard()
            )

    elif query.data == "info":
        keyboard = [[InlineKeyboardButton("⬅️ Retour au menu", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            INFO_TEXT,
            reply_markup=reply_markup
        )

    elif query.data == "back":
        with open("dino.jpg", "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption="🍱 Bienvenue chez DINO TERPS 76\n\n🔥 Accès autorisé\n\nChoisis une option ci-dessous 👇",
                reply_markup=main_keyboard()
            )


# ================================
# Lancement bot
# ================================
def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot lancé 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
