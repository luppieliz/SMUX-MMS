from start import start
from signup import signup_name, signup_gender, gender_m, gender_f
from menu.menu import menu, credits
from schedules import schedules, unregister
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

#Signup CallBacks
updater.dispatcher.add_handler(CommandHandler('signup', signup_name))
updater.dispatcher.add_handler(CallbackQueryHandler(signup_name, pattern='callback_name_edit'))
updater.dispatcher.add_handler(CallbackQueryHandler(signup_gender, pattern='callback_name_confirm'))
updater.dispatcher.add_handler(CallbackQueryHandler(gender_m, pattern='callback_gender_m'))
updater.dispatcher.add_handler(CallbackQueryHandler(gender_f, pattern='callback_gender_f'))

#Menu CallBacks
updater.dispatcher.add_handler(CommandHandler('menu', menu))
updater.dispatcher.add_handler(CallbackQueryHandler(credits, pattern='callback_credits'))

#Schedule Callbacks
updater.dispatcher.add_handler(CommandHandler('schedules', schedules))
updater.dispatcher.add_handler(CallbackQueryHandler(unregister, pattern='callback_unregister'))

#Polling
updater.start_polling()
