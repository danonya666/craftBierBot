import telebot
import telegram
import config
import requests
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
import ssl
from threading import Thread, Lock, current_thread, Event
from time import sleep

from telegram import Bot, TelegramError
from telegram.ext import Dispatcher, JobQueue, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request

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
    update.message.reply_text('WELCOME SIR')
    print("I was here")

def message_response(bot, update):
    bot.send_message(chat_id= update.message.chat_id, text= "Я глупый бот, пока что не умею разговаривать, но скоро "
                                                            "обязательно научусь!")




def main():

    url = '190.15.195.64'
    port = '47912'
    TOKEN = config.api_token
    REQUEST_KWARGS = {
        'proxy_url': 'http://190.53.46.14:56450/' # NEED TO FIND NORMAL PROXY
        #'proxy_url': 'http://' + url + ':' + port + '/',
        # Optional, if you need authentication:
        # 'username': 'PROXY_USER',
        # 'password': 'PROXY_PASS',
    }

    updater = telegram.ext.Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    bot = telebot.TeleBot(config.api_token)
    start_handler = CommandHandler('start', start_callback)
    message_handler = MessageHandler(Filters.text, message_response)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



