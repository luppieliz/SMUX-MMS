from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

#Menu
def menu(update, context):
  update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton("My Profile", callback_data='m1')],
    [InlineKeyboardButton("FAQ", callback_data='m2'),
    InlineKeyboardButton("Credits", callback_data='callback_credits')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
    return 'Main Menu'

#My Profile

#FAQ

#Credits
def credits(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Copyright ©️ Kuebies \n\n Apache License 2.0')