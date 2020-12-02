from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import pyrebase


config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#schedule
def schedules(update, context):
    query = update.callback_query
    query.answer()

    user = db.child('Events').child(update.effective_chat.id).child('Portfolio').get().val()

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

    update.message.reply_text(schedule_menu_message(),
                            reply_markup=main_menu_keyboard_1())


#check after got database, if no scheduled events will open up 
#keyboard with events and activities, if got events then will display the
#events and also the option to unregister the activities.

def got_schedule_keyboard():
    keyboard = [[InlineKeyboardButton("Activites", callback_data='callback_activites'),
    InlineKeyboardButton("Events", callback_data='callback_unregister')]]
    return InlineKeyboardMarkup(keyboard)

def no_schedule_keyboard():
    
    keyboard = [[InlineKeyboardButton("Unregister", callback_data='callback_unregister')]]
    return InlineKeyboardMarkup(keyboard)

def unregister(update, context):
    query = update.callback_query
    query.answer()
    #display the non paid and paid events and the option to unregister
    

def schedule_menu_message():
    return 'Registered Activities'