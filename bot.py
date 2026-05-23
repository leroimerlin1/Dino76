import logging
import json
import os
import asyncio
from datetime import time, timezone, timedelta
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
   MessageHandler,
   filters,
   ContextTypes,
   JobQueue
)

token = "7897439481:AAGl5umeYPVWTMcVxoLdHyO1aY6G0sJ1LK8"

CHANNEL_ID = -1003733915057
CHANNEL_LINK = "https://t.me/+j7EMkLSIaV83ZmU8"
MINI_APP_URL = "https://leroimerlin1.github.io/Dino76/"
GROUP_LINK = "https://t.me/+mktubkoTrqM0ZjI0"

ADMIN_ID = 8313494819

USERS_FILE = "users_dino.json"

# =============================================================
# LOGGING
# =============================================================

logging.basicConfig(
   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
   level=logging.INFO
)

user_logger = logging.getLogger("USER_TRACKER")
user_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("users.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
user_logger.addHandler(file_handler)


# =============================================================
# GESTION DES UTILISATEURS (JSON)
# =============================================================

def load_users() -> dict:
   if os.path.exists(USERS_FILE):
       try:
           with open(USERS_FILE, "r") as f:
               data = json.load(f)
               if isinstance(data, list):
                   return {str(uid): {"first_name": "?", "username": "?"} for uid in data}
               return data
       except Exception:
           return {}
   return {}


def save_user(user_id: int, first_name: str = "?", username: str = None):
   users = load_users()
   users[str(user_id)] = {
       "first_name": first_name,
       "username": username or "?"
   }
   with open(USERS_FILE, "w") as f:
       json.dump(users, f, ensure_ascii=False, indent=2)


# =============================================================
# LOG UTILISATEUR
# =============================================================

def log_user(action: str, user):
   username = f"@{user.username}" if user.username else "Pas de username"
   full_name = user.full_name or "Inconnu"
   msg = f"[{action}] Nom: {full_name} | Username: {username} | ID: {user.id}"
   user_logger.info(msg)
   print(f"👤 {msg}")


# =============================================================
# TEXTE INFORMATION
# =============================================================

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


# =============================================================
# CLAVIER MENU PRINCIPAL
# =============================================================

def main_keyboard():
   keyboard = [
       [
           InlineKeyboardButton("ℹ️ Information", callback_data="info"),
           InlineKeyboardButton("👥 Groupe", url=GROUP_LINK)
       ],
       [
           InlineKeyboardButton("🛍 Boutique", web_app=WebAppInfo(url=MINI_APP_URL))
       ],
       [
           InlineKeyboardButton("📞 Contact", url="https://t.me/dino76s"),
           InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/dinoterps76?igsh=MWlsa2Nkc3lodHVvbg==")
       ]
   ]
   return InlineKeyboardMarkup(keyboard)


# =============================================================
# VÉRIFICATION ABONNEMENT
# =============================================================

async def check_subscription(user_id, context):
   try:
       member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
       return member.status in ["member", "administrator", "creator"]
   except Exception as e:
       print("Erreur vérification abonnement :", e)
       return False


# =============================================================
# HANDLERS
# =============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   if not user:
       return

   log_user("START", user)
   save_user(user.id, first_name=user.first_name or "?", username=user.username)

   is_subscribed = await check_subscription(user.id, context)

   if not is_subscribed:
       keyboard = [
           [InlineKeyboardButton("🔔 Rejoindre le canal", url=CHANNEL_LINK)],
           [InlineKeyboardButton("✅ Vérifier l'abonnement", callback_data="check_sub")]
       ]
       await update.message.reply_text(
           "🦖 DINO TERPS 76\n\n"
           "🔥 Boutique privée premium\n\n"
           "⚠️ Pour accéder à la Mini App, tu dois rejoindre notre canal officiel.",
           reply_markup=InlineKeyboardMarkup(keyboard)
       )
       return

   with open("dino.jpg", "rb") as photo:
       await update.message.reply_photo(
           photo=photo,
           caption="🍱 Bienvenue chez DINO TERPS 76\n\n🔥 Accès autorisé\n\nChoisis une option ci-dessous 👇",
           reply_markup=main_keyboard()
       )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   if not user or user.id != ADMIN_ID:
       await update.message.reply_text("❌ Tu n'as pas la permission d'utiliser cette commande.")
       return

   text = update.message.text.partition("/broadcast")[2].strip()

   if not text:
       await update.message.reply_text(
           "⚠️ Écris ton message après la commande !\n\n"
           "Exemple :\n/broadcast Salut tout le monde 🔥"
       )
       return

   users = load_users()
   if not users:
       await update.message.reply_text("⚠️ Aucun utilisateur enregistré pour l'instant.")
       return

   sent = 0
   failed = 0

   await update.message.reply_text(f"📤 Envoi en cours à {len(users)} utilisateurs...")

   for chat_id in users:
       try:
           await context.bot.send_message(chat_id=int(chat_id), text=text)
           sent += 1
       except Exception as e:
           print(f"Impossible d'envoyer à {chat_id} : {e}")
           failed += 1
       await asyncio.sleep(0.05)

   await update.message.reply_text(
       f"✅ Broadcast terminé !\n\n"
       f"• Envoyés : {sent}\n"
       f"• Échecs : {failed}"
   )


async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   if not user or user.id != ADMIN_ID:
       await update.message.reply_text("❌ Tu n'as pas la permission d'utiliser cette commande.")
       return

   users = load_users()
   if not users:
       await update.message.reply_text("⚠️ Aucun utilisateur enregistré pour l'instant.")
       return

   lines = [f"👥 Utilisateurs enregistrés : {len(users)}\n"]
   for i, (uid, info) in enumerate(users.items(), 1):
       first_name = info.get("first_name", "?")
       username = info.get("username", "?")
       uname_display = f"@{username}" if username != "?" else "pas de @"
       lines.append(f"{i}. {first_name} ({uname_display}) — {uid}")

   message = "\n".join(lines)
   if len(message) <= 4096:
       await update.message.reply_text(message)
   else:
       chunks = []
       current = ""
       for line in lines:
           if len(current) + len(line) + 1 > 4096:
               chunks.append(current)
               current = line
           else:
               current += "\n" + line
       if current:
           chunks.append(current)
       for chunk in chunks:
           await update.message.reply_text(chunk)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   query = update.callback_query
   user = query.from_user
   await query.answer()

   if query.data == "check_sub":
       is_subscribed = await check_subscription(user.id, context)
       if not is_subscribed:
           await query.answer("❌ Tu n'es pas encore abonné.", show_alert=True)
           return

       log_user("ACCÈS CONFIRMÉ (abonnement vérifié)", user)
       save_user(user.id, first_name=user.first_name or "?", username=user.username)

       with open("dino.jpg", "rb") as photo:
           await query.message.reply_photo(
               photo=photo,
               caption="🍱 Accès confirmé !\n\n🔥 Bienvenue dans la boutique exclusive",
               reply_markup=main_keyboard()
           )

   elif query.data == "info":
       log_user("CLIQUE INFO", user)
       keyboard = [[InlineKeyboardButton("⬅️ Retour au menu", callback_data="back")]]
       await query.message.reply_text(INFO_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))

   elif query.data == "back":
       log_user("RETOUR MENU", user)
       with open("dino.jpg", "rb") as photo:
           await query.message.reply_photo(
               photo=photo,
               caption="🍱 Bienvenue chez DINO TERPS 76\n\n🔥 Accès autorisé\n\nChoisis une option ci-dessous 👇",
               reply_markup=main_keyboard()
           )


async def web_app_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   if user:
       log_user("MINI APP OUVERTE", user)


# =============================================================
# LANCEMENT
# =============================================================

def main():
   app = ApplicationBuilder().token(token).build()

   app.add_handler(CommandHandler("start", start))
   app.add_handler(CommandHandler("broadcast", broadcast))
   app.add_handler(CommandHandler("users", users_list))
   app.add_handler(CallbackQueryHandler(button_handler))
   app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_handler))

   print("Bot lancé 🚀")
   app.run_polling()


if __name__ == "__main__":
   main()
