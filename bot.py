word_dig = {'один':1,
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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem
import settings

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update):
    text = 'добро пожаловать в бот, вы нажали /start'
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    if user_text[-1] == '=':
        user_text = user_text.split(' ')
        exp = (user_text[0]).strip('=')
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

        number1 = word_dig[user_text[2]]
        number2 = word_dig[user_text[-1]]
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
        update.message.reply_text(user_text)

def planet(bot, update):
    planets = [i for _0, _1, i in ephem._libastro.builtin_planets()]
    user_text =  update.message.text.split()
    planet_name = planets[user_text[1]]
    if planet_name in planets:
        planet_info = ephem.planet_name()
        reply = print(ephem.constellation(planet_info))
        update.message.reply_text(reply)
    else:
        update.message.reply_text(user_text)

def word_count (bot, update):
    user_text =  update.message.text.split(' ')
    number = 0
    for word in user_text:
        word = word.strip('.,-+-=_:;')
        if word != '':
            number += 1
    number -= 1
    print(number)
    update.message.reply_text('Длина фразы: ' + str(number))

def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)
    logging.info('бот запускается, не торопите, ему надо подумать')


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("wordcount", word_count))
    #dp.add_handler(CommandHandler("calc", calcm))    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()

main()