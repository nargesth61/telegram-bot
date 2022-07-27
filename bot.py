import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import os



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger=logging.getLogger(__name__)

LOCATION, PHOTO, NAME, SERVING, TIME, CONFIRMATION = range(6)
reply_keyboard=[['شروع دوباره','تایید و ادامه']]
markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True,one_time_keyboard=True,)

TOKEN = '5536166739:AAHZcMWeWvjC1oCfsRLO9WqlfoSodpKtewY'
bot = telegram.Bot(token=TOKEN)
chat_id='@nonatestbot'

PORT=int(os.environ.get('PORT ',8003))

def start(update,context):
    user =update
    print(user)

def main():
    updater=Updater(TOKEN,use_context=True)
    dp=updater.dispatcher

    #برای رجیستر دستور استارت بالا
    
    dp.add_handler(CommandHandler('startt',start))
    #برای فعال سازی ربات راهی برای ارتباط با وب اپلیکیشن یا وب سایت ما
    updater.start_webhook(listen='0.0.0.0', port=int(PORT), url_path=TOKEN)
    updater.bot.set_webhook('' + TOKEN)
    
    #دستور زیر ینی تا وقتی ctrl + c را نزنیم ربات فعال باشد
    
    updater.start_polling(timeout=600)
    updater.idle()

#تبدیل دستورات بالا به ماژول

if __name__ == '__main__':
    main()
   