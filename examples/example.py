from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telegram
import re
import json
import requests
import pandas
import bs4
import matplotlib.pyplot as plt
import random
plt.switch_backend('Agg')
import time
def currentTime():
    t0=time.time()
    t1=t0 + 60*60*8
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t1)))

#Alpha Vantage Key
lines = open('keys.txt').read().splitlines()
keys = random.choice(lines)

#WebHook
import os
PORT = int(os.environ.get('PORT', '5000'))
bot = telegram.Bot(token = "1282461089:AAEfAg1-wm8va9KOVlZwbaNlSQiTkpqXdvs")
bot.setWebhook("https://invest-smart.herokuapp.com/" + "1282461089:AAEfAg1-wm8va9KOVlZwbaNlSQiTkpqXdvs")


#Token
updater = Updater(token='1282461089:AAEfAg1-wm8va9KOVlZwbaNlSQiTkpqXdvs', use_context=True)
dispatcher = updater.dispatcher

#Logging Module
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Start Function
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=' Investment Tracker Initialised...')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# I N L I N E  M E N U S

#Menu Function
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

#Portfolio Database
import pyrebase

config = {
    'apiKey': "AIzaSyA7O-5c0M9x23i-JlLrgWqGlgDJ05zfiGc",
    'authDomain': "investsmart-3cd6a.firebaseapp.com",
    'databaseURL': "https://investsmart-3cd6a.firebaseio.com",
    'projectId': "investsmart-3cd6a",
    'storageBucket': "investsmart-3cd6a.appspot.com",
    'messagingSenderId': "180107959220",
    'appId': "1:180107959220:web:e1388c111c0a58d17670e1",
    'measurementId': "G-H7XLMWFS3J"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Favourites/Portfolio (CAN BE STREAMLINED TO RESPOND FASTER)
def faq1(update, context):
    query = update.callback_query
    query.answer()
    user = db.child('Users').child(update.effective_chat.id).child('Portfolio').get().val()

    if user:
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime()))
        portfolio = user.get('stock').rstrip()
        def convert(string):
            li = list(string.split(" "))
            return li
        portfolio_list = convert(portfolio)
        for i in portfolio_list:
            url = 'https://sg.finance.yahoo.com/quote/' + i + '?p=' + i + '&.tsrc=fin-srch'
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
            price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
            context.bot.send_message(chat_id=update.effective_chat.id, text = tickername + '\nCurrent Price: ' + price)

    else:
        query.edit_message_text(text='Your Portfolio is not found. You can begin by using the following command: /save TICK.')

#Credits
def faq3(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Copyright ©️ Jayden Pang \n\n MIT License')

#Where is the data sourced from?
def faq4(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='All price data and news is sourced from Yahoo! Finance. Historical data for graph generation and excel download are procured through Alpha Vantage.')

#What are the current functionalities?
def faq5(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='\
Stock Price & Trend\n\
All US-listed stocks and ETFs can be searched simply by entering the respective tickers. Some results may not produce graphs due to the limitations of Alpha Vantage\'s API. \n\n\
Historical Data Excel Download\n\
The /excel command should be used in conjunction with a ticker in the following format: /excel TICK.\n\n\
You may download historical data with time intervals of 1 minute, 1 hour or 1 day. The bot will not respond to invalid tickers.\n\n\
Technical Indicators\n\
In addition to downloading historical data, you can also quickly access technical indicators for the various tickers via: /indicator TICK. Currently, Simple Moving Average (SMA), Relative Strength Index (RSI)\
 and Bollinger Bands (BBands) are offered.\n\n\
Major Market Indices\n\
The following major market indices can also be quickly accessed through the /index command: DJIA, NASDAQ, S&P500, FTSE and VIX. Only a select few will produce graphs due to API limitations mentioned earlier.\n\n\
Portfolio Function\n\
You can save your favourite tickers in the following fashion: /save TICK. Saved tickers can be found in the Portfolio, located conveniently in /menu. If you wish to remove,\
 simply enter the command in a similar manner: /remove TICK.\n\n\
Latest News\n\
Users can access the latests news on a particular ticker via /news TICK. The five most recent news on Yahoo! Finance will immediately be available for viewing.')

#Why is the bot response slow and certain graphs missing?
def faq6(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='The bot retrieves datas from multiple endpoints, mostly in a raw format which requires parsing before graph generation and eventual output to the end user.\n\n\
As such, the bot response is limited by various factors such as the API calls made, complexity/size of data and internet latency. However, it should not take more than 3 seconds for you to receive a reply from the bot.\n\n\
If that occurs, the bot has encountered an error. The issue mainly arises with graphs and excel downloads where there is reliance on external APIs which does not support all tickers.\
 Unfortunately, such a problem can only be solved on the end of the API creator.')

updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern= 'main'))
#Transition to FAQ Menu
updater.dispatcher.add_handler(CallbackQueryHandler(faq_menu, pattern='m2'))
#Data for Main Menu, Menu Item 1 & Menu Item 3
updater.dispatcher.add_handler(CallbackQueryHandler(faq1, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(faq3, pattern='m3'))
#Data for FAQ Menu, Menu Items 4, 5 & 6
updater.dispatcher.add_handler(CallbackQueryHandler(faq4, pattern='m4'))
updater.dispatcher.add_handler(CallbackQueryHandler(faq5, pattern='m5'))
updater.dispatcher.add_handler(CallbackQueryHandler(faq6, pattern='m6'))
#Menu Command
updater.dispatcher.add_handler(CommandHandler('menu', menu))

#Update Errors
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

updater.dispatcher.add_error_handler(error)

from alpha_vantage.timeseries import TimeSeries
#Price Function
def parsePrice(update, context):
    if len(update.message.text) > 4:
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ticker Support Limit: 4 Characters')
    elif not re.match("^[a-z]*$", update.message.text, re.IGNORECASE):
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ticker Support Only Available for A-Z')    
    else:
        url = 'https://sg.finance.yahoo.com/quote/' + update.message.text + '?p=' + update.message.text + '&.tsrc=fin-srch'
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        if re.search('lookup', res.url):
            context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ticker is invalid, please refer to FAQ for more information.')
        else:
            tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
            price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
            context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime())    + "\n\n" + tickername + '\nCurrent Price: ' + price)
            ts = TimeSeries(key=keys, output_format='pandas')
            data_ts, meta_data_ts = ts.get_intraday(symbol=update.message.text, interval='60min', outputsize='full') # pylint: disable=W0632, W0612
            data_ts['4. close'].plot() # pylint: disable=E1126
            plt.title('Intraday Times Series for the ' + update.message.text.upper() + ' stock (1 hr)')
            plt.savefig('graph.png')
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('graph.png', 'rb'))
            plt.close()


from telegram.ext import MessageHandler, Filters
parsePrice_handler = MessageHandler(Filters.text & (~Filters.command), parsePrice)
dispatcher.add_handler(parsePrice_handler)

import openpyxl
#Excel Menu Function
def data_excel(update, context):
    global uecid
    uecid = update.effective_chat.id
    global umt
    umt = update.message.text
    word = str(umt)
    word_refined = word.replace('/excel ', '')
    if len(umt) <= 7 :
        context.bot.send_message(chat_id=uecid, text = 'Please use /excel command with a ticker: /excel TICK')
    elif len(umt) >= 12:
        context.bot.send_message(chat_id=uecid, text = 'Ticker Support Limit: 4 Characters')
    elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
        context.bot.send_message(chat_id=uecid, text = 'Ticker Support Only Available for A-Z')    
    else:
        update.message.reply_text(excel_menu_message(),
                                reply_markup=excel_menu_keyboard())

#Excel Menu
def excel_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=excel_menu_message(), reply_markup=excel_menu_keyboard())

def excel_menu_keyboard():
    keyboard = [[InlineKeyboardButton("1 Minute", callback_data='e1')],
    [InlineKeyboardButton("1 Hour", callback_data='e2')],
    [InlineKeyboardButton("1 Day", callback_data='e3')]]
    return InlineKeyboardMarkup(keyboard)

def excel_menu_message():
    return 'Please select the historical data time interval you wish to download:'

    

#1 Min Interval
def interval_min(update, context):
    ts = TimeSeries(key=keys, output_format='pandas')
    word = str(umt)
    word_refined = word.replace('/excel ', '')
    data_ts, meta_data_ts = ts.get_intraday(symbol=str(word_refined), interval='1min', outputsize='full') # pylint: disable=W0632, W0612
    data_refined = pandas.DataFrame(data_ts)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='You have downloaded the historical data with time interval of 1 MIN')
    data_refined.to_excel('data.xlsx', sheet_name='DATA (1 MIN)')
    context.bot.send_document(chat_id=uecid, document=open('data.xlsx', 'rb'))

#1 Hr Interval
def interval_hr(update, context):
    ts = TimeSeries(key=keys, output_format='pandas')
    word = str(umt)
    word_refined = word.replace('/excel ', '')
    data_ts, meta_data_ts = ts.get_intraday(symbol=str(word_refined), interval='60min', outputsize='full') # pylint: disable=W0632, W0612
    data_refined = pandas.DataFrame(data_ts)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='You have downloaded the historical data with time interval of 1 HOUR')
    data_refined.to_excel('data.xlsx', sheet_name='DATA (1 HR)')
    context.bot.send_document(chat_id=uecid, document=open('data.xlsx', 'rb'))

#Daily Interval
def interval_day(update, context):
    ts = TimeSeries(key=keys, output_format='pandas')
    word = str(umt)
    word_refined = word.replace('/excel ', '')
    data_ts, meta_data_ts = ts.get_daily(symbol=str(word_refined), outputsize='full') # pylint: disable=W0632, W0612
    data_refined = pandas.DataFrame(data_ts)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='You have downloaded the historical data with time interval of 1 DAY')
    data_refined.to_excel('data.xlsx', sheet_name='DATA (1 DAY)')
    context.bot.send_document(chat_id=uecid, document=open('data.xlsx', 'rb'))


#Callback Query Handler for Excel Menu
updater.dispatcher.add_handler(CallbackQueryHandler(interval_min, pattern='e1'))
updater.dispatcher.add_handler(CallbackQueryHandler(interval_hr, pattern='e2'))
updater.dispatcher.add_handler(CallbackQueryHandler(interval_day, pattern='e3'))

excel_handler = CommandHandler('excel', data_excel)
dispatcher.add_handler(excel_handler)

#Indicators Menu Function
def data_indicator(update, context):
    global uecid
    uecid = update.effective_chat.id
    global umt
    umt = update.message.text
    word = str(umt)
    word_refined = word.replace('/indicator ', '')
    if len(umt) <= 11 :
        context.bot.send_message(chat_id=uecid, text = 'Please use /indicator command with a ticker: /indicator TICK')
    elif len(umt) >= 16:
        context.bot.send_message(chat_id=uecid, text = 'Ticker Support Limit: 4 Characters')
    elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
        context.bot.send_message(chat_id=uecid, text = 'Ticker Support Only Available for A-Z')    
    else:
        update.message.reply_text(indicator_menu_message(),
                                reply_markup=indicator_menu_keyboard())

#Indicator Menu
def indicator_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=indicator_menu_message(), reply_markup=indicator_menu_keyboard())

def indicator_menu_keyboard():
    keyboard = [[InlineKeyboardButton("Simple Moving Average", callback_data='i1')],
    [InlineKeyboardButton("Relative Strength Index", callback_data='i2')],
    [InlineKeyboardButton("Bollinger Bands", callback_data='i3')]]
    return InlineKeyboardMarkup(keyboard)

def indicator_menu_message():
    return 'Please select the technical indictator you wish to display:'

    
from alpha_vantage.techindicators import TechIndicators
#SMA
def sma(update, context):
    ti = TechIndicators(key=keys, output_format='pandas')
    word = str(umt)
    word_refined = word.replace('/indicator ', '')
    data_ti, meta_data_ti = ti.get_sma(symbol=str(word_refined), interval='60min', time_period=60) # pylint: disable=W0632, W0612
    data_refined = pandas.DataFrame(data_ti)
    query = update.callback_query
    query.answer()
    data_refined.plot()
    plt.title('SMA indicator for ' + word_refined + ' stock (60min)')
    plt.savefig('indicator.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('indicator.png', 'rb'))
    plt.close()

#RSI
def rsi(update, context):
    ti = TechIndicators(key=keys, output_format='pandas')
    word = str(umt)
    word_refined = word.replace('/indicator ', '')
    data_ti, meta_data_ti = ti.get_rsi(symbol=str(word_refined), interval='60min', time_period=60) # pylint: disable=W0632, W0612
    data_refined = pandas.DataFrame(data_ti)
    query = update.callback_query
    query.answer()
    data_refined.plot()
    plt.title('RSI indicator for ' + word_refined + ' stock (60min)')
    plt.savefig('indicator.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('indicator.png', 'rb'))
    plt.close()

#BBands
def bbands(update, context):
    ti = TechIndicators(key=keys, output_format='pandas')
    word = str(umt)
    word_refined = word.replace('/indicator ', '')
    data_ti, meta_data_ti = ti.get_bbands(symbol=str(word_refined), interval='60min', time_period=60) # pylint: disable=W0632, W0612
    data_refined = pandas.DataFrame(data_ti)
    query = update.callback_query
    query.answer()
    data_refined.plot()
    plt.title('Bollinger Bands indicator for ' + word_refined + ' stock (60min)')
    plt.savefig('indicator.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('indicator.png', 'rb'))
    plt.close()


#Callback Query Handler for Indicator Menu
updater.dispatcher.add_handler(CallbackQueryHandler(sma, pattern='i1'))
updater.dispatcher.add_handler(CallbackQueryHandler(rsi, pattern='i2'))
updater.dispatcher.add_handler(CallbackQueryHandler(bbands, pattern='i3'))

indicator_handler = CommandHandler('indicator', data_indicator)
dispatcher.add_handler(indicator_handler)

#Save Command for Portfolio
def save(update, context):
    global uecid1
    uecid1 = update.effective_chat.id
    global umt1
    umt1 = update.message.text
    word = str(umt1)
    word_refined = word.replace('/save ', '').upper()
    user = db.child('Users').child(uecid1).get()
    url = 'https://sg.finance.yahoo.com/quote/' + word_refined + '?p=' + word_refined + '&.tsrc=fin-srch'
    res = requests.get(url)
    if not user.val():
        if len(umt1) <= 6:
            context.bot.send_message(chat_id=uecid1, text = 'Please use /save command with a ticker: /save TICK')
        elif len(umt1) >= 11:
            context.bot.send_message(chat_id=uecid1, text = 'Ticker Support Limit: 4 Characters')
        elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
            context.bot.send_message(chat_id=uecid1, text = 'Ticker Support Only Available for A-Z')
        elif re.search('lookup', res.url):
            context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ticker is invalid, please refer to FAQ for more information.') 
        else:
            data_db_first = {
                'stock': word_refined + ' '
            }
            db.child('Users').child(uecid1).child('Portfolio').update(data_db_first)
            context.bot.send_message(chat_id=uecid1, text= word_refined + ' has been saved to Portfolio.')
    else:
        if len(umt1) <= 6:
            context.bot.send_message(chat_id=uecid1, text = 'Please use /save command with a ticker: /save TICK')
        elif len(umt1) >= 11:
            context.bot.send_message(chat_id=uecid1, text = 'Ticker Support Limit: 4 Characters')
        elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
            context.bot.send_message(chat_id=uecid1, text = 'Ticker Support Only Available for A-Z')
        elif re.search('lookup', res.url):
            context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ticker is invalid, please refer to FAQ for more information.') 
        else:
            data_new = db.child('Users').child(uecid1).child('Portfolio').get().val()
            if re.search(r'\b' + word_refined + r'\b', str(data_new.get('stock')), re.IGNORECASE):
                context.bot.send_message(chat_id=uecid1, text= 'Ticker already in Portfolio.')
            else:
                data_new1 = data_new.get('stock') + word_refined + ' '
                data_db_new = {
                    'stock': str(data_new1)
                }
                db.child('Users').child(uecid1).child('Portfolio').update(data_db_new)
                context.bot.send_message(chat_id=uecid1, text= word_refined + ' has been saved to Portfolio.')

#Remove Command for Portfolio
def remove(update, context):
    global uecid2
    uecid2 = update.effective_chat.id
    global umt2
    umt2 = update.message.text
    word = str(umt2)
    word_refined = word.replace('/remove ', '').upper()
    user = db.child('Users').child(uecid2).get()
    if not user.val():
        if len(umt2) <= 8:
            context.bot.send_message(chat_id=uecid2, text = 'Please use /remove command with a ticker: /save TICK')
        elif len(umt2) >= 13:
            context.bot.send_message(chat_id=uecid2, text = 'Ticker Support Limit: 4 Characters')
        elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
            context.bot.send_message(chat_id=uecid2, text = 'Ticker Support Only Available for A-Z')
        else:
            context.bot.send_message(chat_id=uecid2, text= 'There is no ticker in the portfolio to remove.')
    else:
        if len(umt2) <= 8:
            context.bot.send_message(chat_id=uecid2, text = 'Please use /remove command with a ticker: /save TICK')
        elif len(umt2) >= 13:
            context.bot.send_message(chat_id=uecid2, text = 'Ticker Support Limit: 4 Characters')
        elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
            context.bot.send_message(chat_id=uecid2, text = 'Ticker Support Only Available for A-Z')
        else:
            data_new = db.child('Users').child(uecid2).child('Portfolio').get().val()
            if not re.search(r'\b' + word_refined + r'\b', data_new.get('stock'), re.IGNORECASE):
                context.bot.send_message(chat_id=uecid2, text= 'Ticker is not in Portfolio.')
            else:
                data_new2 = data_new.get('stock').replace(word_refined + ' ', '')
                data_db_remove = {
                    'stock': str(data_new2)
                }
                db.child('Users').child(uecid2).child('Portfolio').update(data_db_remove)
                context.bot.send_message(chat_id=uecid2, text= word_refined + ' has been removed to Portfolio.')


save_handler = CommandHandler('save', save)
dispatcher.add_handler(save_handler)
remove_handler = CommandHandler('remove', remove)
dispatcher.add_handler(remove_handler)

#Index Function
def index(update, context):
  update.message.reply_text(index_menu_message(),
                            reply_markup=index_menu_keyboard())

#Index Menu
def index_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=index_menu_message(), reply_markup=index_menu_keyboard())

def index_menu_keyboard():
    keyboard = [[InlineKeyboardButton("DJIA", callback_data='n1')],
    [InlineKeyboardButton("NASDAQ", callback_data='n2')],
    [InlineKeyboardButton("S&P500", callback_data='n3')],
    [InlineKeyboardButton("FTSE", callback_data='n4')],
    [InlineKeyboardButton("VIX", callback_data='n5')]]
    return InlineKeyboardMarkup(keyboard)

def index_menu_message():
    return 'Please choosing from the following Major Market Indices.'

#Index
def djia(update, context):
    query = update.callback_query
    query.answer()
    url = 'https://sg.finance.yahoo.com/quote/%5EDJI?p=^DJI&.tsrc=fin-srch'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
    price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime())    + "\n\n" + tickername + '\nCurrent Price: ' + price)
    ts = TimeSeries(key=keys, output_format='pandas')
    data_ts, meta_data_ts = ts.get_intraday(symbol='DJI', interval='60min', outputsize='full') # pylint: disable=W0632, W0612
    data_ts['4. close'].plot() # pylint: disable=E1126
    plt.title('Intraday Times Series for the DJIA index (1 hr)')
    plt.savefig('index.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('index.png', 'rb'))
    plt.close()

#NASDAQ
def nasdaq(update, context):
    query = update.callback_query
    query.answer()
    url = 'https://sg.finance.yahoo.com/quote/%5EIXIC?p=^IXIC&.tsrc=fin-srch'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
    price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime())    + "\n\n" + tickername + '\nCurrent Price: ' + price)
    ts = TimeSeries(key=keys, output_format='pandas')
    data_ts, meta_data_ts = ts.get_intraday(symbol='IXIC', interval='60min', outputsize='full') # pylint: disable=W0632, W0612
    data_ts['4. close'].plot() # pylint: disable=E1126
    plt.title('Intraday Times Series for the NASDAQ Composite index (1 hr)')
    plt.savefig('index.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('index.png', 'rb'))
    plt.close()

#S&P500
def snp(update, context):
    query = update.callback_query
    query.answer()
    url = 'https://sg.finance.yahoo.com/quote/%5EGSPC?p=^GSPC&.tsrc=fin-srch'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
    price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime())    + "\n\n" + tickername + '\nCurrent Price: ' + price)
    ts = TimeSeries(key=keys, output_format='pandas')
    data_ts, meta_data_ts = ts.get_intraday(symbol='GSPC', interval='60min', outputsize='full') # pylint: disable=W0632, W0612
    data_ts['4. close'].plot() # pylint: disable=E1126
    plt.title('Intraday Times Series for the S&P500 index (1 hr)')
    plt.savefig('index.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('index.png', 'rb'))
    plt.close()

#FTSE
def ftse(update, context):
    query = update.callback_query
    query.answer()
    url = 'https://sg.finance.yahoo.com/quote/%5EFTSE?p=^FTSE&.tsrc=fin-srch'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
    price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime())    + "\n\n" + tickername + '\nCurrent Price: ' + price)
    ts = TimeSeries(key=keys, output_format='pandas')
    data_ts, meta_data_ts = ts.get_intraday(symbol='FTSE', interval='60min', outputsize='full') # pylint: disable=W0632, W0612
    data_ts['4. close'].plot() # pylint: disable=E1126
    plt.title('Intraday Times Series for the FTSE index (1 hr)')
    plt.savefig('index.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('index.png', 'rb'))
    plt.close()

#VIX
def vix(update, context):
    query = update.callback_query
    query.answer()
    url = 'https://sg.finance.yahoo.com/quote/%5EVIX?p=^VIX&.tsrc=fin-srch'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    tickername = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
    price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'CAA ' + str(currentTime())    + "\n\n" + tickername + '\nCurrent Price: ' + price)
    ts = TimeSeries(key=keys, output_format='pandas')
    data_ts, meta_data_ts = ts.get_intraday(symbol='VIX', interval='60min', outputsize='full') # pylint: disable=W0632, W0612
    data_ts['4. close'].plot() # pylint: disable=E1126
    plt.title('Intraday Times Series for the VIX index (1 hr)')
    plt.savefig('index.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('index.png', 'rb'))
    plt.close()

updater.dispatcher.add_handler(CallbackQueryHandler(djia, pattern= 'n1'))
updater.dispatcher.add_handler(CallbackQueryHandler(nasdaq, pattern='n2'))
updater.dispatcher.add_handler(CallbackQueryHandler(snp, pattern='n3'))
updater.dispatcher.add_handler(CallbackQueryHandler(ftse, pattern='n4'))
updater.dispatcher.add_handler(CallbackQueryHandler(vix, pattern='n5'))
#Menu Command
updater.dispatcher.add_handler(CommandHandler('index', index))

#News
import feedparser
def news(update, context):
    global uecid4
    uecid4 = update.effective_chat.id
    global umt4
    umt4 = update.message.text
    word = str(umt4)
    word_refined = word.replace('/news ', '')
    url = 'https://sg.finance.yahoo.com/quote/' + word_refined + '?p=' + word_refined + '&.tsrc=fin-srch'
    res = requests.get(url)
    if len(umt4) <= 6 :
        context.bot.send_message(chat_id=uecid4, text = 'Please use /news command with a ticker: /news TICK')
    elif len(umt4) >= 11:
        context.bot.send_message(chat_id=uecid4, text = 'Ticker Support Limit: 4 Characters')
    elif not re.match("[a-z]*$", word_refined, re.IGNORECASE):
        context.bot.send_message(chat_id=uecid4, text = 'Ticker Support Only Available for A-Z')    
    elif re.search('lookup', res.url):
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ticker is invalid, please refer to FAQ for more information.') 
    else:
        url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=' + word_refined + '&region=US&lang=en-US'
        info = feedparser.parse(url)
        entry = [info.entries[1], info.entries[2], info.entries[3], info.entries[4], info.entries[5]]
        title = [entry[0].title, entry[1].title, entry[2].title, entry[3].title, entry[4].title]
        link = [entry[0].link, entry[1].link, entry[2].link, entry[3].link, entry[4].link]
        context.bot.send_message(chat_id=uecid4, text='Latest News for ' + word_refined.upper() + '\n\n\
<a href="' + link[0] + '">' + title[0] + '</a> \n\n<a href="' + link[1] + '">' + title[1] + '</a>\
\n\n<a href="' + link[2] + '">' + title[2] + '</a> \n\n<a href="' + link[3] + '">' + title[3] + '</a>\
\n\n<a href="' + link[4] + '">' + title[4] + '</a> ', parse_mode='HTML')

news_handler = CommandHandler('news', news)
dispatcher.add_handler(news_handler)


#WebHook
updater.start_webhook(listen="0.0.0.0",
                       port=PORT,
                       url_path="1282461089:AAEfAg1-wm8va9KOVlZwbaNlSQiTkpqXdvs")
updater.bot.setWebhook("https://invest-smart.herokuapp.com/" + "1282461089:AAEfAg1-wm8va9KOVlZwbaNlSQiTkpqXdvs")
updater.idle()

