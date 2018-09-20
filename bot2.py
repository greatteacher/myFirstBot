from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

'''def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    if user_text[-1] == '=':
        user_text = user_text.split(' ')
        exp = (user_text[1]).strip('=')
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
    else:
        update.message.reply_text(user_text)'''




def calc(bot, update):
    user_text = update.message.text
    ans = user_text
    exp, _ = user_text.split('=', 1)
    for i in range(len(exp)):
        if exp[i] in ['+', '-', ':', '*']:
            sign = exp[i]
            number1 = int(exp[:i])
            number2 = int(exp[i + 1: ])
            break
    if sign == '+':
        ans = str(number1 + number2)
    elif sign == '-':
        ans = str(number1 - number2)
    elif sign == ':':
        ans = str(number1 / number2)
    elif sign == '*':
        ans = str(number1 * number2)
    elif user_text.lower().startwith("сколько будет"):
        user_text=user_text.split(' ')
        number1=word_dig[user_text[2]]
        number2=word_dig[user_text[-1]]
        if user_text[3] =='плюс':
            ans = str(number1 + number2)
        elif user_text[3] =='минус':
            ans = str(number1 - number2)
    update.message.reply_text(ans)