import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === LIEN DE LA MINI-APP ===
LIEN_MINI_APP = "https://leroimerlin1.github.io/Dino76/"

# Nom de l'image locale
IMAGE_ACCUEIL = "dino.jpg"

# Clavier avec bouton web app
def get_mini_app_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Ouvrir Mini-App DINO TERPZ 76",
                web_app=WebAppInfo(url=LIEN_MINI_APP)
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat

    keyboard = get_mini_app_keyboard()

    # Vérifie si l'image existe
    if os.path.exists(IMAGE_ACCUEIL):
        with open(IMAGE_ACCUEIL, 'rb') as photo:
            await chat.send_photo(
                photo=photo,
                caption="🦖 Bienvenue sur 🍣DINO TERPZ 76 ! Cliquez ci-dessous pour accéder à la mini-app :",
                parse_mode='Markdown',
                reply_markup=keyboard
            )
    else:
        # Si image manquante, envoie juste le texte
        await chat.send_message(
            "🦖 Bienvenue sur 🍣DINO TERPZ 76 ! Cliquez ci-dessous pour accéder à la mini-app :",
            reply_markup=keyboard
        )

# Gestion erreurs globale
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Erreur inattendue :", exc_info=context.error)

if __name__ == '__main__':
    # Token du bot Telegram
    token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK88041091140:AAGdu3oR3Ag1L_mx_MHytlX4OjfB9wwJ5jo"

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_error_handler(error_handler)

    print("🚀 Bot DINO 76 lancé !")
    application.run_polling()
