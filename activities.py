
from database import db
import logging
import re
from typing import Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, replykeyboardmarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ACTIVTIES,TEAMS,CYCLING,DIVING,KAYAKING,SKATING,TREKKING,XSEED = range(8)

Activites = {
    "Activites" : " "
}
    
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'WANT TO LOOK AT EXCITING ACTIVITIES!!',
    )  
    return ACTIVTIES

def activites(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['CYCLING', 'DIVING'], ['KAYAKING', 'SKATING'], ['TREKING', 'XSEED']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return TEAMS
        
def cycling(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Cycling', 'Diving'], ['Kayaking', 'Skating'], ['Trekking', 'Xseed']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


def diving(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Cycling', 'Diving'], ['Kayaking', 'Skating'], ['Trekking', 'Xseed']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


def kayaking(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Cycling', 'Diving'], ['Kayaking', 'Skating'], ['Trekking', 'Xseed']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


def skating(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Cycling', 'Diving'], ['Kayaking', 'Skating'], ['Trekking', 'Xseed']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


def trekking(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Cycling', 'Diving'], ['Kayaking', 'Skating'], ['Trekking', 'Xseed']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

def xseed(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Cycling', 'Diving'], ['Kayaking', 'Skating'], ['Trekking', 'Xseed']]
    update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bot successfully cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


signup_conv = ConversationHandler(
        entry_points=[
            CommandHandler('Activities', start),],
        states={
            ACTIVTIES:  [CommandHandler('activites', activites)],
            TEAMS: [[MessageHandler(Filters.all)],
                [MessageHandler(CYCLING, cycling)],
                [MessageHandler(DIVING, trekking)],
                [MessageHandler(KAYAKING,kayaking)],
                [MessageHandler(SKATING,skating)],
                [MessageHandler(TREKKING,trekking)],
                [MessageHandler(XSEED,xseed)],
            ],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

dispatcher.add_handler(signup_conv)
