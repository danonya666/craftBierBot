from aifc import Error

import telebot
import telegram

import config
import requests
import logging
import datetime

import keys

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
from config import flag


# Builds menu for buttons that appear in messages sent by bot(InlineKeyboardButtons)
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


# Function for /start command
# Builds a custom cute keyboard
def start_callback(bot, update):
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


# Function responsible for responding to ordinary messages(non-photo-gif-audio BS)
# First 5 strings are just some easter eggs, will delete them probably
def beer_on_bottles(bot, update):
    button_list = [InlineKeyboardButton("По странам", callback_data="bottled beer by countries"),
                   InlineKeyboardButton("По сортам", callback_data="bottled beer by sorts"),
                   InlineKeyboardButton("Полный список", callback_data="bottled beer full list")]
    rM = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    message = bot.send_message(chat_id=update.message.chat_id, text="Как сгруппировать бутылочное пиво?", reply_markup=rM)


def message_response(bot, update):
    cmd = update.effective_message.text
    if cmd == "@CraftBierBot Прости пожалуста":
        bot.send_message(chat_id=update.message.chat_id, text="Я уезжаю в ПРАГУ!")
    elif cmd == "@CraftBierBot Я обиделась!":
        bot.send_message(chat_id=update.message.chat_id, text="Не обижайся дорогая, поехали в ПРАГУ!")
    elif cmd == "Пиво на кране🍺":
        message = beer_on_tap(bot, update)
    elif cmd == "Пиво в бутылках🍾":
        beer_on_bottles(bot, update)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Чего изволите, мой господин?")
    print("----------------------------")
    print(datetime.datetime.now())
    print(update.effective_user.username)
    print(update.effective_message.text)
    print("----------------------------")
    log_msg_to_file(update, "bot_log.txt")



# Removes emoji from the string
# emoji pattern was taken from the internet
def remove_emoji(text):
    return config.emoji_pattern.sub(r'', text)


# noinspection PyBroadException
# Logs sender data and message text to txt file
# TODO: optimize exception system
def log_msg_to_file(update, file):
    f = open(file, 'a')
    f.write("----------------------------" + "\n")
    f.write(str(datetime.datetime.now()) + "\n")
    try:
        f.write(update.effective_user.last_name + "(" + update.effective_user.username + ")" + "\n")
    except:
        try:
            f.write(update.effective_user.last_name)
        except:
            try:
                f.write(update.effective_user.username)
            except:
                f.write(update.effective_user.first_name)
    f.write(remove_emoji(update.effective_message.text) + "\n")
    f.write("----------------------------" + "\n")


# Happens when user taps "Beer on tap" button
# Sends 3-button-menu asking user how to group the beer
def beer_on_tap(bot, update):
    button_list = [InlineKeyboardButton("По странам", callback_data="beer by countries"),
                   InlineKeyboardButton("По сортам", callback_data="beer by sorts"),
                   InlineKeyboardButton("Полный список", callback_data="beer full list")]
    rM = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    message = bot.send_message(chat_id=update.message.chat_id, text="Как сгруппировать пиво на кранах?", reply_markup=rM)
    return message


def beer_on_tap_edit_msg(bot, update, message_id):
    button_list = [InlineKeyboardButton("По странам", callback_data="beer by countries"),
                   InlineKeyboardButton("По сортам", callback_data="beer by sorts"),
                   InlineKeyboardButton("Полный список", callback_data="beer full list")]
    rM = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.edit_message_text(message_id=message_id,
                          chat_id=update.callback_query.message.chat_id, text="Как сгруппировать пиво на кранах?")
    bot.edit_message_reply_markup(message_id=message_id, chat_id=update.callback_query.message.chat_id, reply_markup=rM)


# returns a string with the full beer list
def beer_full_list(beer_list):
    result_string = ""
    for i in beer_list:
        result_string += i.toString()
    return result_string


# Handles the queries incoming from InlineKeyboardButtons
# They come from beer_on_tap section and some others
# Don't know why I use dictionary there, it's not really useful
def bottled_beer_by_counties(beer_list):
    pass


def bottled_beer_by_sorts(beer_list):
    pass


def bottled_beer_full_list(beer_list):
    pass


def query_handler(bot, update):
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    button_list = [InlineKeyboardButton("Назад", callback_data="tab1_back")]
    rM = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    if data == config.query_messages["BbC"]:
        bot.edit_message_text(chat_id=
                              update.callback_query.message.chat_id,
                              message_id=message_id,
                              text=beer_by_countries(beer_list=config.test_beer_list),
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True
                              )
        bot.edit_message_reply_markup(chat_id=
                                      update.callback_query.message.chat_id,
                                      message_id=message_id, reply_markup=rM)
    elif data == config.query_messages["BbS"]:
        bot.edit_message_text(chat_id=
                              update.callback_query.message.chat_id,
                              message_id=message_id,
                              text=beer_by_sorts(beer_list=config.test_beer_list),
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True
                              )
        bot.edit_message_reply_markup(chat_id=
                                      update.callback_query.message.chat_id,
                                      message_id=message_id, reply_markup=rM)
    elif data == config.query_messages["BfL"]:
        bot.edit_message_text(chat_id=
                              update.callback_query.message.chat_id,
                              message_id=message_id,
                              text=beer_full_list(beer_list=config.test_beer_list),
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True
                              )
        bot.edit_message_reply_markup(chat_id=
                                      update.callback_query.message.chat_id,
                                      message_id=message_id, reply_markup=rM)
    elif data == config.query_messages["bBbC"]:
        bot.edit_message_text(chat_id=
                              update.callback_query.message.chat_id,
                              message_id=message_id,
                              text=bottled_beer_by_counties(beer_list=config.test_beer_list),
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True
                              )
        bot.edit_message_reply_markup(chat_id=
                                      update.callback_query.message.chat_id,
                                      message_id=message_id, reply_markup=rM)
    elif data == config.query_messages["bBbS"]:
        bot.edit_message_text(chat_id=
                              update.callback_query.message.chat_id,
                              message_id=message_id,
                              text=bottled_beer_by_sorts(beer_list=config.test_beer_list),
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True
                              )
        bot.edit_message_reply_markup(chat_id=
                                      update.callback_query.message.chat_id,
                                      message_id=message_id, reply_markup=rM)
    elif data == config.query_messages["bBfL"]:
        bot.edit_message_text(chat_id=
                              update.callback_query.message.chat_id,
                              message_id=message_id,
                              text=bottled_beer_full_list(beer_list=config.test_beer_list),
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True
                              )
        bot.edit_message_reply_markup(chat_id=
                                      update.callback_query.message.chat_id,
                                      message_id=message_id, reply_markup=rM)
    elif data == "tab1_back":
        beer_on_tap_edit_msg(bot=bot, update=update, message_id=message_id)


# returns a string that is sent after the query "beers by countries"
# the algorithm is kind of unoptimized, but I guess it's OK for now
def beer_by_countries(beer_list):
    beers_by_countries = [[beer_list[0].country, beer_list[0]]]
    flag = 0
    counter = 0
    for i in beer_list:
        if i == config.first_beer:
            continue
        flag = 0
        counter = 0
        for j in beers_by_countries:
            if j[0] == i.country:
                flag = 1
                beers_by_countries[counter].append(i)
            counter += 1
        if flag == 1:
            pass
        elif flag == 0:
            beers_by_countries.append([i.country, i])
        else:
            print("FLAGERROR")

    print(beers_by_countries)
    result_string = beer_list_by_countries_to_string(beers_by_countries)
    print(result_string)
    return result_string


# converts a [[type, beer, beer, ...], ...] list to a beautiful string that is being sent to user
def beer_list_by_type_to_string(beer_list):
    result_string = ""
    for i in beer_list:
        result_string += i[0].upper() + "🍻" + ": \n\n"
        # print(i[2].toString())
        j = 1
        while j < len(i):
            print(i[j])
            result_string += str(j) + " " + i[j].toString() + " "
            j += 1
    return result_string


# returns a string that is sent after the query "beer_by_sorts"
# unoptimized
def beer_by_sorts(beer_list):
    beers_by_sorts = [[beer_list[0].type, beer_list[0]]]
    flag = 0
    counter = 0
    for i in beer_list:
        if i == config.first_beer:
            continue
        flag = 0
        counter = 0
        for j in beers_by_sorts:
            if j[0] == i.country:
                flag = 1
                beers_by_sorts[counter].append(i)
            ++counter
        if flag == 1:
            pass
        elif flag == 0:
            beers_by_sorts.append([i.type, i])
        else:
            print("FLAGERROR")

    result_string = beer_list_by_type_to_string(beers_by_sorts)
    return result_string


# [[country, beer, beer, ...], ...] -> cute string being sent to user
def beer_list_by_countries_to_string(beer_list):
    result_string = ""
    for i in beer_list:
        result_string += i[0] + flag(i[0]) + ": \n\n"
        # print(i[2].toString())
        j = 1
        while j < len(i):
            print(i[j])
            result_string += str(j) + " " + i[j].toString() + " "
            j += 1
    return result_string


def main():
    TOKEN = keys.api_token  # CraftBierBot api token

    # for proxy
    # there are some OK proxies in config.proxy_list
    # they are not mine, but I don't think it's bad to use them ;)
    REQUEST_KWARGS = {
        'proxy_url': config.proxy_list[0]  # NEED TO FIND NORMAL PROXY
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
    updater.idle()  # not sure this string is necessary, but it works, so I'm keeping it


if __name__ == '__main__':
    main()
