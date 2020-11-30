from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

#Start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to SMUX's Membership Management System, ")