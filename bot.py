#%%
from dotenv import load_dotenv
import os
import telebot
import requests
from bs4 import BeautifulSoup

import atexit
from apscheduler.schedulers.background import BackgroundScheduler


class HouseBot:

    def __init__(self):

        # load all environments
        load_dotenv()

        self.TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
        self.bot = telebot.TeleBot(self.TELEGRAM_API_KEY)
        self.INTERVAL_SECONDS = 60 * 60 * 6 # hours

        # print(self.TELEGRAM_API_KEY)

        # Handle /start command
        @self.bot.message_handler(commands=["start"])
        def start_command(message):
            
            # run the function once
            self.fetch_data(message)

            # run it with an interval
            self.scheduler = BackgroundScheduler(timezone="Europe/Berlin")
            self.scheduler.add_job(func=lambda: self.fetch_data(message), id="fetch_data", trigger="interval", seconds=self.INTERVAL_SECONDS)
            self.scheduler.start()

            atexit.register(lambda: self.scheduler.shutdown())


        # Handle /start command
        @self.bot.message_handler(commands=["stop"])
        def stop_command(message):
            self.scheduler.pause_job(job_id='fetch_data')
            
        self.bot.polling()

    def fetch_data(self, message):

        page = requests.get("https://www.berlinovo.de/en/housing/search")
        soup = BeautifulSoup(page.content, 'html.parser')

        source_count = soup.find('span', class_='source-summary-count').get_text()
        titles_soup = soup.find_all('div', class_='block-field-blocknodeapartmenttitle')
        titles = [title.div.span.a.get_text() for title in titles_soup]

        data = {}
        data["source_count"] = source_count
        data["titles"] = titles

        result = str(data["source_count"]) + "\n" +  str(data["titles"])

        self.bot.send_message(message.chat.id, result)


def create_app():
    """
    this function is for production environments
    """
    app = HouseBot()
    return app


# page = requests.get("https://www.berlinovo.de/en/housing/search")
# page.content

# soup = BeautifulSoup(page.content, 'html.parser')
# source_count = soup.find('span', class_='source-summary-count').get_text()

# titles = soup.find_all('div', class_='block-field-blocknodeapartmenttitle')
# availabilities = soup.find_all('div', class_='field--name-field-available-date')
# availabilities = soup.find_all('div', class_='field--name-field-available-date')
# postal_codes = soup.find_all('div', class_='field--name-field-available-date')
# warm_rents = soup.find_all('div', class_='field--name-field-available-date')

# print(source_count)
# [title.div.span.a.get_text() for title in titles]
# [availability.find_all("div", {"class": "field__item"}) for availability in availabilities]
