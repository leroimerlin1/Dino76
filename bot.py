import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Récupère le token depuis l'environnement
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Erreur : La variable d'environnement BOT_TOKEN n'est pas définie !")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Fonction qui répond à la commande /start
    en envoyant un bouton pour ouvrir la mini-app
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Ouvrir Mini-App DINO 76",
                web_app=WebAppInfo(url="https://leroimerlin1.github.io/Dino76/")
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🦖 Bienvenue sur DINO 76 ! Cliquez ci-dessous pour accéder à la mini-app :",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tapez /start pour ouvrir la mini-app DINO 76.")

# Crée l'application du bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Ajouter les handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

print("🤖 Bot DINO 76 démarré !")

# Lancement du polling
app.run_polling()
