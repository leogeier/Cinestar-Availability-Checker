import requests
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Updater, CommandHandler
from telegram import Bot
import sqlite3

NOT_AVAILABLE_INDICATOR = 'Dieser Film befindet sich aktuell nicht im Programm.'
DB_FILE = 'database.sqlite'

def querySite(url, name, bot):
    r = requests.get(url)

    sendMessage = NOT_AVAILABLE_INDICATOR not in r.text
    text = "🚨🚨🚨 '{}' TICKETS ARE AVAILIBLE! 🚨🚨🚨".format(name)
    if not r.status_code == requests.codes.ok:
        text = "ATTENTION: Status code is not OK!"
        sendMessage = True

    if sendMessage:
        print("Sending message...")
        # Warn all groups
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("""SELECT chat_id
            FROM entry""")
        for result in c.fetchall():
            bot.send_message(chat_id=result[0], text=text)

def id_in_db(db, chat_id):
    c = db.cursor()
    c.execute("""SELECT count(1)
        FROM entry
        WHERE chat_id=?""",
              (chat_id,))
    return c.fetchone()[0] != 0

def registerGroup(bot, update):
    try:
        db = sqlite3.connect(DB_FILE)
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
        db = sqlite3.connect(DB_FILE)
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

    # Set up bot
    with open('.bot-token.txt') as f:
        token = f.read()
        updater = Updater(token=token)
        bot = Bot(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('register', registerGroup))
    dispatcher.add_handler(CommandHandler('unregister', unregisterGroup))

    # Set up scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(querySite, 'interval', seconds=interval, args=[url, name, bot])
    scheduler.start()

    print("Start polling...")
    updater.start_polling()
    updater.idle()
