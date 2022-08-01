import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import os



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger=logging.getLogger(__name__)

LOCATION, PHOTO, NAME, SERVING, TIME, CONFIRMATION = range(6)

reply_keyboard=[['شروع دوباره','مورد تایید است']]
markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True,one_time_keyboard=True,)


TOKEN = '5536166739:AAHZcMWeWvjC1oCfsRLO9WqlfoSodpKtewY'
bot = telegram.Bot(token=TOKEN)
chat_id='@nonatestbot'

def facts_to_str(user_data):
   facts = list()
   for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))
        
   return "\n".join(facts).join(['\n', '\n']) 


def start(update,context):
    update.message.reply_text('.سلام من ربات دستیار شما برای کمک به حیوانات هستم.با کمک من غذاهای اضافی خودتونو به حیوونای بی پناه بدید.واسه شروع ادرستو بفرس')
    
    return LOCATION

def location(update, context):
   user = update.message.from_user
   user_data =context.user_data
   category ='آدرس'
   text = update.message.text
   user_data[category]=text

   logger.info("Location of %s: %s", user.first_name, update.message.text)
    
   update.message.reply_text("خب؛ اگر تصویری از غذا داری ارسال کن اگر نه از /skip استفاده کن تا این مرحله رو رد کنی")
   return PHOTO

def photo(update, context):
    user=update.message.from_user
    user_data =context.user_data
    photo_file=update.message.photo[-1].get_file()
    photo_file.download('food_photo.jpg')
    category = 'تصویر دارد'
    user_data[category] = 'بله'
    
    logger.info("Photo of %s: %s", user.first_name, 'food_photo.jpg')
    
    update.message.reply_text('بسیار عالی؛ اسم غذا چیه')
    return NAME


def skip_photo(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'تصویر دارد'
    user_data[category] = 'نه'
    
    logger.info("User %s did not send an photo", user.first_name)
    
    update.message.reply_text('بسیار عالی؛ اسم غذا چیه')
    
    return NAME

def food_name(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'نام غذا'
    text = update.message.text
    user_data[category] = text
    
    logger.info("Name of the food is %s", text)
    
    update.message.reply_text('چقدر زمان میبرد تا غذا را تحویل دهید')
    
    
    return SERVING

def serving(update, context):
    user =update.message.from_user
    user_data =context.user_data
    category = ' مقدار غذا چقدر است'
    text=update.message.text
    user_data[category] = text
    
    logger.info("Name of the servings %s", text)
    update.message.reply_text('از نظر شمااین غذا برای چند حیوان قابل استفاده است')
    return TIME

def time(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'چقدر زمان می برد تا غذا آماده شود'
    text = update.message.text
    user_data[category] = text
    
    logger.info("Time to take Food by %s", text)
    
    update.message.reply_text('از این که اطلاعات را برای ما ارسال کردین سپاس گزاریم . لطفا بررسی کنید که آیا اطلاعات مورد تاییدتان است یا نه {}'.format(facts_to_str(user_data)), 
                              reply_markup=markup) 
    
    return CONFIRMATION

def confirmation(update, context):
    user = update.message.from_user
    user_data=context.user_data
    update.message.reply_text('از شما سپاس گزاریم اطلاعات شما بر روی کانال ' + chat_id + ' ارسال شد.',reply_markup=ReplyKeyboardRemove())
    
    if (user_data['تصویر دارد'] == 'بله'):
        del user_data['تصویر دارد']
        bot.send_photo(chat_id=chat_id, photo=open('food_photo.jpg', 'rb'), 
                       caption='<b> این غذا در دسترس است</b> جزءیات در زیر ذکر شده \n {}'.format(facts_to_str(user_data)) + 
                       "\n برای اطلاعات بیشتر با ارسال کننده در ازتباط باشید {}".format(user.name), 
                       parse_mode=telegram.ParseMode.HTML)
    
    else:
        del user_data['تصویر دارد']
        bot.send_message(chat_id=chat_id, text='<b> این غذا در دسترس است</b> جزءیات در زیر ذکر شده \n {}'.format(facts_to_str(user_data)) + 
                       "\n برای اطلاعات بیشتر با ارسال کننده در ازتباط باشید {}".format(user.name), 
                       parse_mode=telegram.ParseMode.HTML)
        
    
    return ConversationHandler.END

def cancele(update, context):
    user = update.message.from_user
    update.message.reply_text('از ارتباط شما ممنونیم',reply_markup=ReplyKeyboardRemove())
    
    return ConversationHandler.END

def error(update, context):
     logger.warning('Update "%s" caused error "%s"', update, context.error)
    

def main():
    updater=Updater(TOKEN,use_context=True)
    dp=updater.dispatcher
    
    conver_handler=ConversationHandler(
        entry_points =[CommandHandler("start", start)],
        
        states ={
            LOCATION:[CommandHandler('start', start), MessageHandler(Filters.text, location)],
            PHOTO:[CommandHandler('start', start), MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            NAME:[CommandHandler('start',start),MessageHandler(Filters.text,food_name)],
            SERVING:[CommandHandler('start',start),MessageHandler(Filters.text,serving)],
            TIME:[CommandHandler('start',start),MessageHandler(Filters.text,time)],
            CONFIRMATION:[CommandHandler('start', start), MessageHandler(Filters.regex('^مورد تایید است$'), confirmation), 
                          MessageHandler(Filters.regex('^شروع دوباره$'), start)]
            },
        fallbacks =[CommandHandler('cancele',cancele)]
    )

    dp.add_handler(conver_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

#تبدیل دستورات بالا به ماژول

if __name__ == '__main__':
    main()
   