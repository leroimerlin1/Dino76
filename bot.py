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

CHANNEL_ID = -1003733915057  # Mets le vrai ID
CHANNEL_LINK = "https://t.me/+j7EMkLSIaV83ZmU8"
MINI_APP_URL = "https://leroimerlin1.github.io/Dino76/"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

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

    # ✅ ABONNÉ
    keyboard = [
        [InlineKeyboardButton("🛍 Ouvrir la boutique", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🍱 Bienvenue chez DINO TERPS 76\n\n"
        "🔥 Accès autorisé\n\n"
        "Clique ci-dessous pour ouvrir la boutique 👇",
        reply_markup=reply_markup
    )


# ================================
# Bouton Vérifier abonnement
# ================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    is_subscribed = await check_subscription(query.from_user.id, context)

    if not is_subscribed:
        await query.answer("❌ Tu n'es pas encore abonné.", show_alert=True)
        return

    keyboard = [
        [InlineKeyboardButton("🛍 Ouvrir la boutique", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🍱 Accès confirmé !\n\n"
        "🔥 Bienvenue dans la boutique exclusive 👇",
        reply_markup=reply_markup
    )


# ================================
# Lancement bot
# ================================
def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="check_sub"))

    print("Bot lancé 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
