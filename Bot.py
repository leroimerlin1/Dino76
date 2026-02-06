const TelegramBot = require('node-telegram-bot-api');

const token = '8041091140:AAGdu3oR3Ag1L_mx_MHytlX4OjfB9wwJ5jo';
const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '🦖 Bienvenue sur DINO 76', {
    reply_markup: {
      inline_keyboard: [[
        {
          text: '🚀 Mini-app DINO 76',
          web_app: {
            url: 'https://tonpseudo.github.io/dino76/'
          }
        }
      ]]
    }
  });
});
