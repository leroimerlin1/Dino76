import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    InputFile
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK8"
CHANNEL_USERNAME = "https://t.me/+j7EMkLSIaV83ZmU8"  # ex: @dinoterps76
MINI_APP_URL = "https://leroimerlin1.github.io/Dino76/"  # URL de ta mini app

logging.basicConfig(level=logging.INFO)


# Vérifier abonnement
async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    is_subscribed = await check_subscription(user.id, context)

    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("🔔 Rejoindre le canal", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("✅ Vérifier", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚠️ Tu dois rejoindre notre canal pour accéder à la boutique.",
            reply_markup=reply_markup
        )
        return

    # S'il est abonné → envoyer image + texte + mini app
    keyboard = [
        [InlineKeyboardButton("🛍 Ouvrir la boutique", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=InputFile("dino.jpg"),
        caption="🍱 Bienvenue chez DINO TERPS 76\n\n🔥 Accède à notre boutique exclusive ci-dessous 👇",
        reply_markup=reply_markup
    )


# Vérification bouton
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    is_subscribed = await check_subscription(query.from_user.id, context)

    if not is_subscribed:
        await query.edit_message_text(
            "❌ Tu n'es toujours pas abonné au canal."
        )
        return

    keyboard = [
        [InlineKeyboardButton("🛍 Ouvrir la boutique", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_photo(
        photo=InputFile("dino.jpg"),
        caption="🍱 Accès autorisé !\n\n🔥 Clique ci-dessous pour entrer dans la boutique 👇",
        reply_markup=reply_markup
    )


def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(button_handler, pattern="check_sub"))

    print("Bot lancé...")
    app.run_polling()


if __name__ == "__main__":
    main()
