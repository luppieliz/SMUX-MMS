##MY PROFILE MODULE
##NOK

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

NAME, HPNUM, RELATIONSHIP, EDIT, EDIT_NAME_END, EDIT_HPNUM_END, EDIT_RELATIONSHIP_END = range(7)

nokinfo = {
    "name" : "",
    "hpnum" : "",
    "relationship" : "",
}


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'The following section is regards to you Next-of-Kin (NOK) details.\n\n'
        'NOK Name:',
        reply_markup=ReplyKeyboardRemove()
    )

    return NAME

def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["name"] = update.message.text
    logger.info("NOK name of %s: %s", nokinfo['name'], update.message.text)
    update.message.reply_text(
        'NOK Contact Number (e.g 91234567):',
        reply_markup=ReplyKeyboardRemove()
        )

    return HPNUM

def hpnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["hpnum"] = update.message.text
    logger.info("NOK contact number of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Relationship of NOK (e.g. Father, Mother):',
        reply_markup=ReplyKeyboardRemove()
    )

    return RELATIONSHIP

def relationship(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["relationship"] = update.message.text
    logger.info("NOK relationship of  %s: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())

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
        'NOK Name:',
    )

    return EDIT_NAME_END

def edit_name_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["name"] = update.message.text
    logger.info("%s edited their NOK name to: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_hpnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'NOK Contact Number (e.g 91234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_HPNUM_END

def edit_hpnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["hpnum"] = update.message.text
    logger.info("%s edited their NOK contact number to: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_relationship_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Relationship of NOK (e.g. Father, Mother):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_RELATIONSHIP_END

def edit_relationship_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["relationship"] = update.message.text
    logger.info("%s edited their NOK relationship to: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def editnokinfo_message() ->str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/Name: {nokinfo['name']}\n"
    output += f"/HP_Number: {nokinfo['hpnum']}\n"
    output += f"/Relationship: {nokinfo['relationship']}\n"
    
    return output

def done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("%s confirmed their NOK details. Uploading to database.", user.first_name)
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

def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1225082753:AAEBkXHqkTWUwrnTr7ez86temk2AVoypJCE", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('nok', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            HPNUM: [MessageHandler(Filters.text & ~Filters.command, hpnum)],
            RELATIONSHIP: [MessageHandler(Filters.text & ~Filters.command, relationship)],
            EDIT: [
                CommandHandler('done', done),
                CommandHandler('Name', edit_name_start),
                CommandHandler('HP_Number', edit_hpnum_start),
                CommandHandler('Relationship', edit_relationship_start),
            ],
            EDIT_NAME_END: [MessageHandler(Filters.text & ~Filters.command, edit_name_end)],
            EDIT_HPNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_hpnum_end)],
            EDIT_RELATIONSHIP_END: [MessageHandler(Filters.text & ~Filters.command, edit_relationship_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
