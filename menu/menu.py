from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

def menu(update, context):
  update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

#Main Menu
def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=main_menu_message(), reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton("Favourites", callback_data='m1')],
    [InlineKeyboardButton("FAQ", callback_data='m2'),
    InlineKeyboardButton("Credits", callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
    return 'Main Menu'

#FAQ Menu
def faq_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=faq_menu_message(), reply_markup=faq_menu_keyboard())

def faq_menu_keyboard():
    keyboard = [[InlineKeyboardButton("Where is the data sourced from?", callback_data='m4')],
    [InlineKeyboardButton("What are the current functionalities?", callback_data='m5')],
    [InlineKeyboardButton("Why is the bot response slow and certain graphs missing?", callback_data='m6')],
    [InlineKeyboardButton("Return to Main Menu", callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def faq_menu_message():
    return 'FAQ Menu'