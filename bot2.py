from emoji import emojize
import ephem
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


def greet_user(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_data['smile'] = smile 
    text = 'Привет {}'.format(smile)
    contact_button = KeyboardButton('Пришли контакты', request_contact=True)
    location_button = KeyboardButton('Пришли локацию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика','/start', 'Сменить авку' ],
                                        [contact_button,location_button]
                                       ]
                                      ) # то что отображается на кнопке можно добавить чтобы кнопка поменьше , resize_keyboard=True
    # Прислать фотки котика
    update.message.reply_text(text, reply_markup=get_keyboard()) # удалить скобку и коменты , reply_markup=my_keyboard)


def talk_to_me(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_text = "Hello, {} {}! Ты написалa: {}".format(update.message.chat.first_name,  user_data['smile'],
                    update.message.text) 
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                    update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard()) # отправляет тот же самый текст в телеграмм, что польз-ль написал


def send_Daniel_picture(bot, update, user_data):
    Dan_list = glob('Daniel/Daniel*.jp*g')
    Dan_pic = choice(Dan_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'), reply_markup=get_keyboard()) #read binory читать двоичную 

def change_avatar(bot, update, user_data):
    if 'smile' in user_data:
        del user_data['smile']
    smile = get_user_smile(user_data)
    update.message.reply_text('ready: {}'.format(smile), reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    print(update. message.contact)
    update.message.reply_text('ready: {}'.format(smile), reply_markup=get_keyboard())

  
def get_location(bot, update, user_data):
    print(update. message.location)
    update.message.reply_text('ready: {}'.format(smile), reply_markup=get_keyboard())
  

def get_user_smile(user_data):
    if "smile" in user_data:
        return user_data['smile']
    else: 
        user_data['smile'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['smile']


def get_keyboard():
    contact_button = KeyboardButton('Пришли контакты', request_contact=True)
    location_button = KeyboardButton('Пришли локацию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика','/start', 'Сменить авку' ],
                                        [contact_button,location_button]
                                       ], resize_keyboard=True
                                      )     
    return my_keyboard
def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)
    logging.info('бот запускается, не торопите, ему надо подумать')

    dp = mybot.dispatcher # сокращаю майбот.диспетчер, чтбы не писать 100 раз
    dp.add_handler(CommandHandler("start", greet_user,pass_user_data=True))
    # dp.add_handler(CommandHandler("calc", calcm))    
    dp.add_handler(CommandHandler("daniel", send_Daniel_picture))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_Daniel_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить авку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
