from dotenv import load_dotenv
import os
import telebot

import atexit
from apscheduler.schedulers.background import BackgroundScheduler


class HouseBot:

    def __init__(self):

        # load all environments
        load_dotenv()

        self.TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
        self.bot = telebot.TeleBot(self.TELEGRAM_API_KEY)
        

        # Handle /start command
        @self.bot.message_handler(commands=["start"])
        def start_command(message):
            data = self.fetch_data()

            result = data["result"]
            
            # run the function once
            self.reply_to_bot(message, result)

            # run it with an interval
            self.scheduler = BackgroundScheduler(timezone="Europe/Berlin")
            self.scheduler.add_job(func=lambda: self.reply_to_bot(message, result), trigger="interval", seconds=1) #60 * 60)
            self.scheduler.start()

            atexit.register(lambda: self.scheduler.shutdown())


        # Handle /start command
        @self.bot.message_handler(commands=["stop"])
        def stop_command(message):
            self.scheduler.shutdown()
            
        self.bot.polling()

    def reply_to_bot(self, message, output):
        self.bot.reply_to(message, output)

    def fetch_data(self):

        data = {}
        data["result"] = 5 + 5

        return data

house_bot = HouseBot()


