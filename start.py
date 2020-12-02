from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

#Start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to SMUX's Membership Management System, You may begin accessing your account via /menu. For more information regarding functionalities, please use /faq.")