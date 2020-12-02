from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


#first time user splash
# def signup(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome first time user. Please fill in your profile details. Who can see this information: Only you, and the present EXCO of SMUX. By filling in the following fields, you agree to entrust your information with SMUX and its managing members.")

#Name

def signup_name(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome first time user. Please fill in your profile details. Who can see this information: Only you, and the present EXCO of SMUX.\n\nBy filling in the following fields, you agree to entrust your information with SMUX and its managing members.")
    context.bot.send_message(chat_id=update.effective_chat.id, text=signup_name_message())
    name = update.message.text
    #db add name
    if name:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Is {name} correct?", reply_markup=signup_name_confirm_buttons())

def signup_name_message():
    return 'Please enter your matriculated name:'

from telegram.ext import MessageHandler, Filters
signup_name_handler = MessageHandler(Filters.text & (~Filters.command), signup_name)
dispatcher.add_handler(signup_name_handler)

def signup_name_confirm_buttons():
    keyboard = [InlineKeyboardButton("Yes", callback_data='callback_name_confirm'),
    InlineKeyboardButton("No", callback_data='callback_name_edit')]
    return InlineKeyboardMarkup(keyboard)

#Gender
def signup_gender(update, context):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=update.effective_chat.id, text=signup_gender_message(), reply_markup=signup_gender_buttons())

def signup_gender_buttons():
    keyboard = [InlineKeyboardButton("Male", callback_data='callback_gender_m'),
    InlineKeyboardButton("Female", callback_data='callback_gender_f')]
    return InlineKeyboardMarkup(keyboard)

def signup_gender_message():
    return 'What is your gender?'

def gender_m(update, context):
    query = update.callback_query
    query.answer()
    #db add gender m
    query.edit_message_text(text='You are male! <next field>')

def gender_f(update, context):
    query = update.callback_query
    query.answer()
    #db add gender f
    query.edit_message_text(text='You are female! <next field>')