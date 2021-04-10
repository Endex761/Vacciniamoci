from message_generator import MessageGenerator
import logging
import time
from database import Database

import telegram
from telegram.ext import Updater, CommandHandler

from settings import *

class Bot:

    def __init__(self, token, messageGenerator: MessageGenerator):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.logger = logging.getLogger("LOG")
        self.logger.info("Starting BOT.")
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.messageGenerator = messageGenerator
        messageGenerator.generate()
        self.message = self.messageGenerator.get_message()

        self.job = self.updater.job_queue

        self.job_daily = self.job.run_daily(callback=self.send_daily_message, time=DAILY_TIME, days=(0,1,2,3,4,5,6), context=None, name=None)

        start_handler = CommandHandler("start", self.send_start)
        self.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler("help", self.send_help)
        self.dispatcher.add_handler(help_handler)

        enable_handler = CommandHandler("enable", self.send_enable)
        self.dispatcher.add_handler(enable_handler)

        disable_handler = CommandHandler("disable", self.send_disable)
        self.dispatcher.add_handler(disable_handler)

        message_handler = CommandHandler("news", self.send_message)
        self.dispatcher.add_handler(message_handler)

        # daily_handler = CommandHandler("daily", self.send_daily)
        # self.dispatcher.add_handler(daily_handler)

    # message to send when the bot is started
    def send_start(self, chatbot, update):
        welcome_message =  '*Ciao, sono il bot che tiene traccia dei vaccini!*\n\n'
        welcome_message += '✔ Digita: /enable per ricevere informazioni giornaliere riguardo lo stato delle vaccinazioni in italia!\n\n'
        welcome_message += '❌ Digita: /disable per non ricevere più le informazioni giornaliere.\n\n'
        welcome_message += '📰 Digita: /news per visualizzare lo stato attuale.\n\n'
        welcome_message += '⚙ Digita: /help per ulteriori informazioni.'
        chatbot.message.reply_text(welcome_message, parse_mode = telegram.ParseMode.MARKDOWN)

    # message to send when /help is received
    def send_help(self, chatbot, update):
        welcome_message =  'Author: @Simon761\n'
        welcome_message += 'Fonte dei dati: https://github.com/italia/covid19-opendata-vaccini/blob/master/dati\n'
        welcome_message += 'Gli aggiornamenti giornalieri avvengono alle ore 18:00'
        chatbot.message.reply_text(welcome_message, parse_mode = telegram.ParseMode.MARKDOWN)
       
    # message to send when /enable is received
    def send_enable(self, chatbot, update):
        # write the chat id in the database
        chat_id = chatbot.message.chat_id
        db = Database()
        db.add_user(chat_id)
        db.close()
        # send the confermation message
        enable_message = 'Riceverai informazioni ogni giorno alle 18:00!'
        chatbot.message.reply_text(enable_message)
    
    # message to send when /disable is received
    def send_disable(self, chatbot, update):
        # remove chat id from the database
        chat_id = chatbot.message.chat_id
        db = Database()
        db.rem_user(chat_id)
        db.close()
        # send the confermation message
        goodbye_message = 'Non riceverai più messaggi dal bot.'
        chatbot.message.reply_text(goodbye_message)

    
    def send_message(self, chatbox, update):
        chatbox.message.reply_text(self.message, parse_mode = telegram.ParseMode.MARKDOWN)

    # send the daily message to the subscribed users
    def send_daily_message(self, chatbot):
        # update the message 
        self.update_message()

        # get subscribers chat_ids
        db = Database()
        users = db.get_users()
        db.close()

        # send updated message to subscribers
        for user in users:
            try:
                chat_id = user[0]
                chatbot.bot.send_message(chat_id, self.message, parse_mode = telegram.ParseMode.MARKDOWN)

                # sleep 35 millisecond to prevent ban for spam
                time.sleep(0.035)
            except Exception:
                logging.warning(f"Error sending message for chat_id: {chat_id}.")
        
    # update the message to send daily
    def update_message(self):
        self.messageGenerator.update()
        self.message = messageGenerator.get_message()

    # start the bot
    def run(self):
        self.logger.info("Polling BOT.")
        self.updater.start_polling()

        # Run the BOT until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the BOT gracefully.
        self.updater.idle()
        return 0


if __name__ == "__main__":
    TOKEN = get_token()
    messageGenerator = MessageGenerator()
    BOT = Bot(TOKEN, messageGenerator)
    BOT.run()
