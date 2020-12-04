#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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

SIGNUP, NAME, GENDER, MATNUM, HPNUM, EMAIL, BLOODTYPE, MEDICAL, DIETARY, EDIT, EDIT_NAME_END, EDIT_GENDER_END, EDIT_MATNUM_END, EDIT_HPNUM_END, EDIT_EMAIL_END, EDIT_BLOODTYPE_END, EDIT_MEDICAL_END, EDIT_DIETARY_END = range(18)

userinfo = {
    "name" : "",
    "gender" : "",
    "matnum" : "",
    "hpnum" : "",
    "email" : "",
    "bloodtype" : "",
    "medical" : "",
    "dietary" : "",
}

def print_userinfo(userinfo: Dict[str, str]) -> str:
    output = list()

    for key, value in userinfo.items():
        output.append(f'{key} {value}')

    return "\n".join(output).join(['\n', '\n'])

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Hi! Test SMUX bot here. I will collect your data for registration.\n\n'
        'Send /signup to begin the sign up process and /cancel to stop the bot.',
    )

    return SIGNUP

def signup(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Full name (according to matriculation):',
    )  
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["name"] = update.message.text
    logger.info("Matriculated name of %s: %s", userinfo['name'], update.message.text)
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'Select gender:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["gender"] = update.message.text
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Matriculation number:',
        reply_markup=ReplyKeyboardRemove(),
    )

    return MATNUM

def matnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["matnum"] = update.message.text
    logger.info("Matriculation number of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Contact number (e.g.: 91234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return HPNUM

def hpnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["hpnum"] = update.message.text
    logger.info("Contact number of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'SMU email address (e.g. johntan.2020@sis.smu.edu.sg):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EMAIL

def email(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    user = update.message.from_user
    userinfo["email"] = update.message.text
    logger.info("Email of  %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Blood Type:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return BLOODTYPE

def bloodtype(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["bloodtype"] = update.message.text
    logger.info("Blood type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your prevailing medical conditions, or '/skip' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return MEDICAL

def medical(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["medical"] = update.message.text
    logger.info("Medical situatiton of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your dietary requirements, or '/skip' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DIETARY

def skip_medical(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["medical"] = "NA"
    logger.info("%s has no medical conditions.", user.first_name)
    update.message.reply_text(
        "Enter your dietary requirements, or '/skip' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DIETARY

def dietary(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["dietary"] = update.message.text
    logger.info("Dietary requirements of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

def skip_dietary(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["dietary"] = "NA"
    logger.info("%s has no dietary requirements", user.first_name)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

#==============================================================================================#
                            #  _______  ______  __________________ #
                            # (  ____ \(  __  \ \__   __/\__   __/ #
                            # | (    \/| (  \  )   ) (      ) (    #
                            # | (__    | |   ) |   | |      | |    #
                            # |  __)   | |   | |   | |      | |    #
                            # | (      | |   ) |   | |      | |    #
                            # | (____/\| (__/  )___) (___   | |    #
                            # (_______/(______/ \_______/   )_(    #
                            #                                      #
#==============================================================================================#


def edit_name_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Full name (according to matriculation):',
    )

    return EDIT_NAME_END

def edit_name_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["name"] = update.message.text
    logger.info("%s edited their matriculated name to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_gender_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'Select gender:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_GENDER_END

def edit_gender_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["gender"] = update.message.text
    logger.info("%s edited their gender to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_matnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Matriculation number:',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_MATNUM_END

def edit_matnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["matnum"] = update.message.text
    logger.info("%s edited their matriculation number to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_hpnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Contact number (e.g.: 91234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_HPNUM_END

def edit_hpnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["hpnum"] = update.message.text
    logger.info("%s edited their contact number to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_email_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'SMU email address (e.g. johntan.2020@sis.smu.edu.sg):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_EMAIL_END

def edit_email_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["email"] = update.message.text
    logger.info("%s edited their email to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_bloodtype_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    update.message.reply_text(
        'Blood Type:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_BLOODTYPE_END

def edit_bloodtype_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["bloodtype"] = update.message.text
    logger.info("%s edited their blood type to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_medical_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your medical conditions. If there are none, please enter "None".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_MEDICAL_END

def edit_medical_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["medical"] = update.message.text
    logger.info("%s edited their medical condition to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_dietary_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your dietary requirements. If there are none, please enter "None".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_DIETARY_END

def edit_dietary_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["dietary"] = update.message.text
    logger.info("%s edited their dietary requirements to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edituserinfo_message() ->str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/Name: {userinfo['name']}\n"
    output += f"/Gender: {userinfo['gender']}\n"
    output += f"/Matriculation_Number: {userinfo['matnum']}\n"
    output += f"/HP_Number: {userinfo['hpnum']}\n"
    output += f"/Email: {userinfo['email']}\n"
    output += f"/Blood_Type: {userinfo['bloodtype']}\n"
    output += f"/Medical_Conditions: {userinfo['medical']}\n"
    output += f"/Dietary_Restrictions: {userinfo['dietary']}\n"
    
    return output

def done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("%s confirmed their details. Uploading to database.", user.first_name)
    #database push!
    update.message.reply_text(
        "Information confirmed.",
        reply_markup=ReplyKeyboardRemove(),
    )
    #how to integrate back into main menu

    return ConversationHandler.END


#==============================================================================================#

# Fallback commands (return to all other menus), remember to integrate with main functions

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bot successfully cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

#==============================================================================================#


conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CommandHandler('signup', signup)],
    states={
        SIGNUP:  [CommandHandler('signup', signup)],
        NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
        GENDER: [MessageHandler(Filters.regex('^(Male|Female)$'), gender)],
        MATNUM: [MessageHandler(Filters.text & ~Filters.command, matnum)],
        HPNUM: [MessageHandler(Filters.text & ~Filters.command, hpnum)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        BLOODTYPE: [MessageHandler(Filters.regex('^(O\+|O\-|AB\+|AB\-|A\+|A\-|B\+|B\-)$'), bloodtype)],
        MEDICAL: [
            MessageHandler(Filters.text & ~Filters.command, medical),
            CommandHandler('skip', skip_medical),
        ],
        DIETARY: [
            MessageHandler(Filters.text & ~Filters.command, dietary),
            CommandHandler('skip', skip_dietary),
        ],
        EDIT: [
            CommandHandler('done', done),
            CommandHandler('Name', edit_name_start),
            CommandHandler('Gender', edit_gender_start),
            CommandHandler('Matriculation_Number', edit_matnum_start),
            CommandHandler('HP_Number', edit_hpnum_start),
            CommandHandler('Email', edit_email_start),
            CommandHandler('Blood_Type', edit_bloodtype_start),
            CommandHandler('Medical_Conditions', edit_medical_start),
            CommandHandler('Dietary_Restrictions', edit_dietary_start),
        ],
        EDIT_NAME_END: [MessageHandler(Filters.text & ~Filters.command, edit_name_end)],
        EDIT_GENDER_END: [MessageHandler(Filters.regex('^(Male|Female)$'), edit_gender_end)],
        EDIT_MATNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_matnum_end)],
        EDIT_HPNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_hpnum_end)],
        EDIT_EMAIL_END: [MessageHandler(Filters.text & ~Filters.command, edit_email_end)],
        EDIT_BLOODTYPE_END: [MessageHandler(Filters.regex('^(O\+|O\-|AB\+|AB\-|A\+|A\-|B\+|B\-)$'), edit_bloodtype_end)],
        EDIT_MEDICAL_END: [MessageHandler(Filters.text & ~Filters.command, edit_medical_end)],
        EDIT_DIETARY_END: [MessageHandler(Filters.text & ~Filters.command, edit_dietary_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
