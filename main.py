from start import start
from menu import menu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

#Logging Module
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Token
updater = Updater(token='1395949263:AAECQtjOsNWQUeIyHL02JhmIyoGNRw1Txt8', use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(CommandHandler('menu', menu))
\
#Polling
updater.start_polling()
