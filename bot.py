from dotenv import load_dotenv
import os
import telebot

# load all environments
load_dotenv()

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=["answer"])
def greet(message):
    bot.reply_to(message, "Yes, I am answering.")

@bot.message_handler(commands=["greet me"])
def greet(message):
    bot.send_message(message.chat.id, "Hey! Hows it going?")

bot.polling()