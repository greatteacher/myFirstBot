#from emoji import emojize
#import ephem
from glob import glob
import logging
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



def greet_costumer():
    #contact_button = KeyboardButton('Пришли контакты', request_contact=True)
    #location_button = KeyboardButton('Пришли локацию', request_location=True)
    text = 'Выбери кофе'
    my_keyboard = ReplyKeyboardMarkup([
                                        ['pizza' ],
                                        ['sweets','coffee']
                                        # ,[contact_button,location_button]
                                       ], resize_keyboard=True
                                      )     
    update.message.reply_text(text, reply_markup=my_keyboard)


def keyboard_coffee(bot, update):
    # contact_button = KeyboardButton('Пришли контакты', request_contact=True)
    # location_button = KeyboardButton('Пришли локацию', request_location=True)
    text = 'Привет, что бы вы хотели из кофейка?'    
    my_button = ReplyKeyboardMarkup([
                                        ['на главную', 'корзина'],
                                        ['Americano' ,'Гляссе'],
                                        ['Capuccino','Latte']
                                        # ,[contact_button,location_button]
                                       ], resize_keyboard=True
                                      )
    update.message.reply_text(text, reply_markup = my_button) # удалить скобку и коменты , reply_markup=my_keyboard)




def send_Americano_description(bot, update):
    Dan_list = glob('coffee/coffee1*.jp*g')
    Dan_pic = choice(Dan_list)
    text = 'just black coffee'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))


def send_Capuccino_description(bot, update):
    Dan_list = glob('coffee/coffee2*.jp*g')
    Dan_pic = choice(Dan_list)
    text = 'coffee with milk'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))

def send_Latte_description(bot, update):
    Dan_list = glob('coffee/coffee3*.jp*g')
    Dan_pic = choice(Dan_list)
    text = 'coffee rich of milk, more than in Capuccino'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))


def send_Glase_description(bot, update):
    Glase_list = glob('coffee/coffee4*.jp*g')
    Glase_pic = choice(Glase_list)
    text = 'coffee with spoon of ice-cream'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Glase_pic, 'rb'))


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('бот запускается, не торопите, ему надо подумать')

    dp = mybot.dispatcher # сокращаю майбот.диспетчер, чтбы не писать 100 раз
    dp.add_handler(CommandHandler('start', greet_costumer)) #, pass_user_data=True))
    dp.add_handler(CommandHandler('coffee', keyboard_coffee)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(на главную)$', greet_costumer)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Americano)$', send_Americano_description)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(Capuccino)$', send_Capuccino_description)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Гляссе)$', send_Glase_description)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Latte)$', send_Latte_description)) #, pass_user_data=True))
    #dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    #dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    #dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()