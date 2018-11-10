from aifc import Error

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

from telegram import Bot, TelegramError, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Dispatcher, JobQueue, CommandHandler, MessageHandler, Filters, InlineQueryHandler, \
    ConversationHandler, CallbackQueryHandler
from telegram.utils.request import Request
from beer import Beer

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


def start_callback(bot, update):
    button_list = [InlineKeyboardButton("Пиво на кране🍺", switch_inline_query_current_chat="Даешь пиво на кране"),
                   InlineKeyboardButton("Пиво в бутылках🍾", switch_inline_query_current_chat="Даёшь пиво в бутылках"),
                   InlineKeyboardButton("Еда🍔", switch_inline_query_current_chat="Даёшь еду и побыстрее"),
                   InlineKeyboardButton("Бронь🗓", switch_inline_query_current_chat="Даёшь бронь столиков"),
                   InlineKeyboardButton("Контакты📞", switch_inline_query_current_chat="Даёшь номер босса!"),
                   InlineKeyboardButton("Время работы⏱", switch_inline_query_current_chat="Скажи, когда вы работаете?"),
                   InlineKeyboardButton("Оценить💯", switch_inline_query_current_chat="Дай-ка я вас оценю!"),
                   ]

    keyboard_button_list = [[KeyboardButton("Пиво на кране🍺"), KeyboardButton("Пиво в бутылках🍾")], [KeyboardButton(
        'Еда🍔'), KeyboardButton("Бронь🗓")], [KeyboardButton("Контакты📞"), KeyboardButton("Время работы⏱")],
                            ["Оценить💯"]]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    # rep_key_markup = telegram.ReplyKeyboardMarkup(keyboard=button_list)
    bot.send_message(chat_id=update.message.chat_id, text=config.welcoming_string,  # reply_markup=reply_markup)
                     reply_markup=telegram.ReplyKeyboardMarkup(keyboard=keyboard_button_list, one_time_keyboard=False,
                                                               resize_keyboard=False))

    # LOGGING IN CONSOLE
    print("----------------------------")
    print(datetime.datetime.now())
    print(update.effective_user.username)
    print(update.effective_message.text)
    print("----------------------------")

    # LOGGING TO FILE
    log_msg_to_file(update, "bot_log.txt")


def message_response(bot, update):
    cmd = update.effective_message.text
    if cmd == "@CraftBierBot Прости пожалуста":
        bot.send_message(chat_id=update.message.chat_id, text="Я уезжаю в ПРАГУ!")
    elif cmd == "@CraftBierBot Я обиделась!":
        bot.send_message(chat_id=update.message.chat_id, text="Не обижайся дорогая, поехали в ПРАГУ!")
    elif cmd == "Пиво на кране🍺":
        beer_on_tap(bot, update)
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


def beer_on_tap(bot, update):
    button_list = [InlineKeyboardButton("По странам", callback_data="beer by countries"),
                   InlineKeyboardButton("По сортам", callback_data="beer by sorts"),
                   InlineKeyboardButton("Полный список", callback_data="beer full list")]
    rM = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(chat_id=update.message.chat_id, text="Как сгруппировать пиво?", reply_markup=rM)


def query_handler(bot, update):
    if update.callback_query.data == config.query_messages["BbC"]:
        bot.send_message(chat_id=
                         update.callback_query.chat_instance, text=" ".join("".join(beer_by_countries(beer_list=config.test_beer_list)))
        )

def beer_by_countries(beer_list):
    beers_by_countries = [[beer_list[0].country, beer_list[0].name]]
    flag = 0
    counter = 0
    for i in beer_list:
        flag = 0
        counter = 0
        for j in beers_by_countries:
            if j[0] == i.country:
                flag = 1
                beers_by_countries[counter].append(i)
            ++counter
        if flag == 1:
            pass
        elif flag == 0:
            beers_by_countries.append([i.country, i.name])
        else:
            print("FLAGERROR")

    return beers_by_countries


def main():
    my_beer_list = []
    my_beer_list.append(Beer("Meizels Weisse", "Germany", "some brewery", 10, 5.5))
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
    callback_query_handler = CallbackQueryHandler(callback=query_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(callback_query_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
