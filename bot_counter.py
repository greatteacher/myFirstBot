from emoji import emojize
import ephem
from glob import glob
import logging
from random import choice
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

import settings


WORD_DIGITS_MAP = {
    'один':1,
    'два':2, 
    'три' :3,
    'четыре':4,
    'пять':5,
    'шесть':6,
    'семь':7,
    'восемь':8,
    'девять':9,
    'десять':10
}


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    smile = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_data['smile'] = smile 
    text = 'Привет {}'.format(smile)
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика','/start', 'Сменить авку' ]]) # то что отображается на кнопке можно добавить чтобы кнопка поменьше , resize_keyboard=True
    # Прислать фотки котика
    update.message.reply_text(text, reply_markup=my_keyboard) # удалить скобку и коменты , reply_markup=my_keyboard)


def change_avatar(bot, update, user_data):
    if 'smile' in user_data:
        del user_data('smile')
    smile = get_user_smile(user_data)
    update.message.reply_text('ready: {}'.format(smile))


def get_user_smile(user_data):
    if "smile" in user_data:
        return user_data['smile']
    else: 
        user_data['smile'] = emojize(choice(settings.USER_EMOJI, use_aliases=True))
        return user_data['smile']


def talk_to_me(bot, update, user_data):
    user_text = "Hello, {} {}! Ты написал: {}".format(update.message.chat.first_name, user_data['smile'], update.message.text) 
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.id, update.message.text)
    print(user_text)
    if user_text[-1] == '=':
        user_text = user_text.split(' ')
        exp = (user_text[0]).strip('=')
        # for char in exp:
        for i in range(len(exp)):
            if exp[i] in ['+', '-', '/', '*']:
                sign = exp[i]
                number1 = int(exp[:i])
                number2 = int(exp[i + 1: ])
                break
        if sign == '+':
            result = number1 + number2
        elif sign == '-':
            result = number1 - number2
        elif sign == '*':
            result = number1 * number2
        elif sign == '/':
            result = number1 / number2
        print (result)
        update.message.reply_text(str(result))

    elif user_text.lower().startswith ('когда ближайшее полнолуние после'):
        user_text = user_text.split()
        date = user_text[-1].replace('-', '/').strip ('?')
        moon = ephem.next_full_moon(date)
        print(moon)
        update.message.reply_text(moon)

    elif user_text.lower().startswith ('сколько будет'):
        user_text = user_text.split(' ')

        number1 = WORD_DIGITS_MAP[user_text[2]]
        number2 = WORD_DIGITS_MAP[user_text[-1]]
        if user_text[3] == 'плюс':
            result = number1 + number2
        elif user_text[3] == 'минус':
            result = number1 - number2
        elif user_text[3] == 'умножить':
            result = number1 * number2
        elif user_text[3] == 'разделить':
            result = number1 / number2
        print (result)
        update.message.reply_text(str(result))
    else:
        update.message.reply_text(user_text) # отправляет тот же самый текст в телеграмм, что польз-ль написал


def planet(bot, update, user_data):
    planets = [i for _0, _1, i in ephem._libastro.builtin_planets()]
    user_text =  update.message.text.split()
    planet_name = planets[user_text[1]]
    if planet_name in planets:
        planet_info = ephem.planet_name()
        reply = print(ephem.constellation(planet_info))
        update.message.reply_text(reply)
    else:
        update.message.reply_text(user_text)


def word_count (bot, update, user_data):
    user_text =  update.message.text.split(' ')
    number = -1 # starts to count from comand, i dont need it
    for word in user_text:
        word = word.strip('.,-+-=_:;')
        if word != '':
            number += 1
    update.message.reply_text('Длина фразы: ' + str(number))


def send_Daniel_picture(bot, update, user_data):
    Dan_list = glob('Daniel/Daniel*.jp*g')
    Dan_pic = choice(Dan_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb')) #read binory читать двоичную 


def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)
    logging.info('бот запускается, не торопите, ему надо подумать')

    dp = mybot.dispatcher # сокращаю майбот.диспетчер, чтбы не писать 100 раз
    dp.add_handler(CommandHandler("start", greet_user,pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planet,pass_user_data=True))
    dp.add_handler(CommandHandler("wordcount", word_count,pass_user_data=True))
    # dp.add_handler(CommandHandler("calc", calcm))    
    dp.add_handler(CommandHandler("daniel", send_Daniel_picture))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_Daniel_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить авку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
