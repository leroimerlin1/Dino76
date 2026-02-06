import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.error import NetworkError, TimedOut

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === TES LIENS ===
LIEN_CANAL_TELEGRAM = "https://t.me/+Bn-Ly265PCtkMTM0"
LIEN_VITRINE = "https://callup.luffa.im/c/PtoS5qYZefe"
LIEN_CONTACT = "https://t.me/Sav_qualityfarmz76"

# === IMAGE LOCALE ===
NOM_IMAGE = "quality.jpg"

# Claviers
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Menu", callback_data='menu')],
        [
            InlineKeyboardButton("📢 Canal Telegram", url=LIEN_CANAL_TELEGRAM)
        ],
        [
            InlineKeyboardButton("📸 Vitrine", url=LIEN_VITRINE),
            InlineKeyboardButton("✉️ Contact", url=LIEN_CONTACT)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_menu_with_back_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Menu", callback_data='menu')],
        [
            InlineKeyboardButton("📢 Canal Telegram", url=LIEN_CANAL_TELEGRAM)
        ],
        [
            InlineKeyboardButton("📸 Vitrine", url=LIEN_VITRINE),
            InlineKeyboardButton("✉️ Contact", url=LIEN_CONTACT)
        ],
        [InlineKeyboardButton("🔙 Retour", callback_data='accueil')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Textes
TEXTE_ACCUEIL = """
🌟 **Bienvenue !** 🌟

Voici les liens utiles de **Qualityfarmz76**

Choisis une option ci-dessous 👇
"""

TEXTE_MENU = """
**📋 Menu principal**

**🧽Jaune mousseux🧽**
**Kinder Maxi🍫🥚**

**10G = 50€**
**25G = 110€**
**50G = 150€**
**100G = 280€**
"""

# Fonction accueil robuste
async def envoyer_accueil(chat):
    try:
        if os.path.exists(NOM_IMAGE):
            with open(NOM_IMAGE, 'rb') as photo:
                await chat.send_photo(
                    photo=photo,
                    caption=TEXTE_ACCUEIL,
                    parse_mode='Markdown',
                    reply_markup=get_main_menu_keyboard()
                )
            return
    except Exception as e:
        logger.error(f"Erreur image accueil : {e}")

    await chat.send_message(
        TEXTE_ACCUEIL,
        parse_mode='Markdown',
        reply_markup=get_main_menu_keyboard()
    )

# /start et /menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await envoyer_accueil(update.message.chat)

# Gestion des boutons (CORRIGÉE POUR LE RETOUR)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # On essaie de supprimer l'ancien message, mais on ignore les erreurs
    try:
        await query.message.delete()
    except:
        pass  # Si ça échoue (message déjà supprimé ou trop vieux), on continue quand même

    if query.data == 'menu':
        try:
            if os.path.exists(NOM_IMAGE):
                with open(NOM_IMAGE, 'rb') as photo:
                    await query.message.chat.send_photo(
                        photo=photo,
                        caption=TEXTE_MENU,
                        parse_mode='Markdown',
                        reply_markup=get_menu_with_back_keyboard()
                    )
                return
        except Exception as e:
            logger.error(f"Erreur image menu : {e}")

        await query.message.chat.send_message(
            TEXTE_MENU,
            parse_mode='Markdown',
            reply_markup=get_menu_with_back_keyboard()
        )

    elif query.data == 'accueil':
        # Retour forcé à l'accueil, même si suppression a échoué
        await envoyer_accueil(query.message.chat)

# Gestion erreurs globale
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Erreur inattendue :", exc_info=context.error)
    # On n'envoie plus de message d'erreur pour les petites exceptions courantes
    # (le bot gère déjà tout en interne)

if __name__ == '__main__':
    application = ApplicationBuilder().token("8433304578:AAHTAtyqw7ZnzK-2QymALBgohAZNTXmwa8g").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_error_handler(error_handler)

    print("🚀 Bot Qualityfarmz76 lancé – Bouton Retour corrigé !")
    application.run_polling()
