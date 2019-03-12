import requests
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Updater, CommandHandler
from telegram import Bot

NOT_AVAILABLE_INDICATOR = 'Dieser Film befindet sich aktuell nicht im Programm.'

def querySite(url):
    r = requests.get(url)
    if NOT_AVAILABLE_INDICATOR not in r.text:
        print("alarm")

def ping_(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="pong")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: [URL] [Interval in seconds] [name]")
        sys.exit()

    # Extract arguments
    url = sys.argv[1]
    interval = int(sys.argv[2])
    name = sys.argv[3]

    # Set up scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(querySite, 'interval', seconds=interval, args=[url])
    scheduler.start()

    # Set up bot
    with open('.bot-token.txt') as f:
        token = f.read()
        updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('ping', ping_))

    updater.start_polling()
    updater.idle()
