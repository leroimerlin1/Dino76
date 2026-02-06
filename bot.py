const TelegramBot = require('node-telegram-bot-api');

const token = 'NOUVEAU_TOKEN_ICI';
const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/start/, (msg) => {
  console.log("Commande /start reçue");

  bot.sendMessage(msg.chat.id, '🦖 Bienvenue sur DINO 76', {
    reply_markup: {
      inline_keyboard: [[
        {
          text: '🚀 Mini-app DINO 76',
          web_app: {
            url: 'https://leroimerlin1.github.io/Dino76/'
          }
        }
      ]]
    }
  });
});

bot.on('message', (msg) => {
  console.log("Message reçu :", msg.text);
});
