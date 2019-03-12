import requests
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Updater, CommandHandler
from telegram import Bot
import sqlite3

NOT_AVAILABLE_INDICATOR = 'Dieser Film befindet sich aktuell nicht im Programm.'

def querySite(url):
    r = requests.get(url)
    if NOT_AVAILABLE_INDICATOR not in r.text:
        print("alarm")

def id_in_db(db, chat_id):
    c = db.cursor()
    c.execute("""SELECT count(1)
        FROM entry
        WHERE chat_id=?""",
              (chat_id,))
    return c.fetchone()[0] != 0

def registerGroup(bot, update):
    try:
        db = sqlite3.connect('database.sqlite')
        chat_id = update.message.chat_id
        if not id_in_db(db, chat_id):
            db.execute("""INSERT INTO entry
                VALUES (?)""",
                       (chat_id,))
            db.commit()
        bot.send_message(chat_id=update.message.chat_id, text="I registered this group!")
    except Error:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I could not register this group!")

def unregisterGroup(bot, update):
    try:
        db = sqlite3.connect('database.sqlite')
        chat_id = update.message.chat_id
        if id_in_db(db, chat_id):
            db.execute("""DELETE FROM entry
                WHERE chat_id=?""",
                       (update.message.chat_id,))
            db.commit()
        bot.send_message(chat_id=update.message.chat_id, text="I unregistered this group!")
    except Error:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I could not unregister this group!")

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
    dispatcher.add_handler(CommandHandler('register', registerGroup))
    dispatcher.add_handler(CommandHandler('unregister', unregisterGroup))

    updater.start_polling()
    updater.idle()
