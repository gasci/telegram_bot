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
            
            # run the function once
            self.fetch_data(message)

            # run it with an interval
            self.scheduler = BackgroundScheduler(timezone="Europe/Berlin")
            self.scheduler.add_job(func=lambda: self.fetch_data(message), id="fetch_data", trigger="interval", seconds=1) #60 * 60)
            self.scheduler.start()

            atexit.register(lambda: self.scheduler.shutdown())


        # Handle /start command
        @self.bot.message_handler(commands=["stop"])
        def stop_command(message):
            self.scheduler.pause_job(job_id='fetch_data')
            
        self.bot.polling()

    def fetch_data(self, message):
        data = {}
        data["result"] = 5 + 5
        result = data["result"]

        self.bot.reply_to(message, result)

house_bot = HouseBot()


