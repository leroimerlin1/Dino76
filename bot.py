# -*- coding: utf-8 -*-
"""
Bot Telegram simple qui envoie :
- Ta Mini App Telegram
- Une image dino.jpg avec texte
- Réagit au mot "token" ou à la commande /token
"""

import logging
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ────────────────────────────────────────────────
#  CONFIGURATION - À MODIFIER
# ────────────────────────────────────────────────

token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK8"                     # ← Remplace par TON VRAI TOKEN BOT

# URL de ta Mini App (obtenue via @BotFather → Menu Button ou Web App)
MINI_APP_URL = "https://ton-site.com/miniapp/index.html"   # ← METS TON VRAI LIEN ICI

# Chemin vers l'image (local ou URL)
DINO_IMAGE_PATH = "dino.jpg"        # fichier local
# ou bien : DINO_IMAGE_URL = "https://ton-site.com/dino.jpg"

# Texte qui accompagne l'image
IMAGE_CAPTION = (
    "🏆 Dino Terps 76\n"
    "🥇 Produits premium - Frozen Sift & Cali 🇺🇸\n"
    "🚚 Livraison Normandie & Meet-up\n"
    "👇 Clique sur le bouton ci-dessous pour ouvrir la boutique !"
)

# ────────────────────────────────────────────────

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /start"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="Ouvrir la boutique Dino Terps 76 🍃",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Salut ! Bienvenue chez Dino Terps 76 🏆\n"
        "Clique sur le bouton pour ouvrir la boutique :",
        reply_markup=reply_markup
    )


async def send_miniapp_and_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envoie la mini app + l'image dino.jpg"""
    # Bouton Mini App
    keyboard = [
        [
            InlineKeyboardButton(
                text="Ouvrir la boutique 🍃",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoi de l'image avec caption + bouton
    if Path(DINO_IMAGE_PATH).is_file():
        # Image locale
        await update.message.reply_photo(
            photo=open(DINO_IMAGE_PATH, 'rb'),
            caption=IMAGE_CAPTION,
            reply_markup=reply_markup
        )
    else:
        # Sinon message simple (image non trouvée)
        await update.message.reply_text(
            IMAGE_CAPTION,
            reply_markup=reply_markup
        )


async def token_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Réagit quand on écrit "token" ou /token"""
    await send_miniapp_and_image(update, context)


def main():
    application = Application.builder().token(token).build()

    # Commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("token", token_trigger))

    # Message contenant "token" (insensible à la casse)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Regex(r'(?i)\btoken\b'),
            token_trigger
        )
    )

    # Pour lancer le bot
    print("Bot démarré... (Ctrl+C pour arrêter)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
