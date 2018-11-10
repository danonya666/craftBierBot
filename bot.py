import telebot
import telegram

import config
import requests
import logging
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
import ssl
from threading import Thread, Lock, current_thread, Event
from time import sleep

from telegram import Bot, TelegramError, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, JobQueue, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def get_updates_json(request):
    response = requests.get(request + "getUpdates")
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def send_message(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(config.url + 'sendMessage', data=params)
    return response


def start_callback(bot, update):
    button_list = [InlineKeyboardButton("Пиво на кране🍺", switch_inline_query_current_chat="Даешь пиво на кране"),
                   InlineKeyboardButton("Пиво в бутылках🍾", switch_inline_query_current_chat="Даёшь пиво в бутылках"),
                   InlineKeyboardButton("Еда🍔", switch_inline_query_current_chat="Даёшь еду и побыстрее"),
                   InlineKeyboardButton("Бронь🗓", switch_inline_query_current_chat="Даёшь бронь столиков"),
                   InlineKeyboardButton("Контакты📞", switch_inline_query_current_chat="Даёшь номер босса!"),
                   InlineKeyboardButton("Время работы⏱", switch_inline_query_current_chat="Скажи, когда вы работаете?"),
                   InlineKeyboardButton("Оценить💯", switch_inline_query_current_chat="Дай-ка я вас оценю!"),
                   ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text=config.welcoming_string, reply_markup=reply_markup)

    # LOGGING
    print("----------------------------")
    print(datetime.datetime.now())
    print(update.effective_user.username)
    print(update.effective_message.text)
    print("----------------------------")


def message_response(bot, update):
    if update.effective_message.text == "@CraftBierBot Прости пожалуста":
        bot.send_message(chat_id=update.message.chat_id, text="Я уезжаю в ПРАГУ!")
    elif update.effective_message.text == "@CraftBierBot Я обиделась!":
        bot.send_message(chat_id=update.message.chat_id, text="Не обижайся дорогая, поехали в ПРАГУ!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Чего изволите, мой Господин?")
    print("----------------------------")
    print(datetime.datetime.now())
    print(update.effective_user.username)
    print(update.effective_message.text)
    print("----------------------------")
    log_msg_to_file(update, "bot_log.txt")


def log_msg_to_file(update, file):
    f = open(file, 'a')
    f.write("----------------------------" + "\n")
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(update.effective_user.first_name + " ")
    f.write(update.effective_user.last_name + "(" + update.effective_user.username + ")" + "\n")
    f.write(update.effective_message.text + "\n")
    f.write("----------------------------" + "\n")


def main():
    url = '190.15.195.64'
    port = '47912'
    TOKEN = config.api_token
    REQUEST_KWARGS = {
        'proxy_url': 'http://69.70.219.202:56946/'  # NEED TO FIND NORMAL PROXY
        # 'proxy_url': 'http://' + url + ':' + port + '/',
        # Optional, if you need authentication:
        # 'username': 'PROXY_USER',
        # 'password': 'PROXY_PASS',
    }

    updater = telegram.ext.Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    start_handler = CommandHandler('start', start_callback)
    message_handler = MessageHandler(Filters.text, message_response)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
