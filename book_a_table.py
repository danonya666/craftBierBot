import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import results

now = datetime.datetime.now()
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


def make_dates_menu(bot, update):
    now = datetime.datetime.now()
    now_day = now.day
    now_month = now.month
    curr_month = now_month
    odd_months = [1, 3, 5, 7, 8, 10, 12]
    if now_month in odd_months:
        month_capacity = 31
    elif now_month == 2 and now.year % 4 == 0:
        month_capacity = 29
    elif now_month == 2:
        month_capacity = 28
    else:
        month_capacity = 30
    print(month_capacity)
    button_list = []
    i = now_day
    button_counter = 0
    button_list.append(InlineKeyboardButton(text="ПН", callback_data="blank"))
    button_list.append(InlineKeyboardButton(text="ВТ", callback_data="blank"))
    button_list.append(InlineKeyboardButton(text="СР", callback_data="blank"))
    button_list.append(InlineKeyboardButton(text="ЧТ", callback_data="blank"))
    button_list.append(InlineKeyboardButton(text="ПТ", callback_data="blank"))
    button_list.append(InlineKeyboardButton(text="СБ", callback_data="blank"))
    button_list.append(InlineKeyboardButton(text="ВС", callback_data="blank"))
    button_counter += 7
    button_list.append(InlineKeyboardButton(text=i, callback_data=i))
    i += 1
    button_counter += 1
    while i != now_day:
        button_list.append(InlineKeyboardButton(text=i, callback_data=i))
        i += 1
        button_counter += 1
        if i > month_capacity:
            i = 1
            curr_month += 1

    while button_counter % 7 != 0:
        button_list.append(InlineKeyboardButton(text=" ", callback_data="blank"))
        button_counter += 1
    rM = InlineKeyboardMarkup(build_menu(button_list, n_cols=7))

    msg_id = update.message.message_id
    bot.send_message(chat_id=update.message.chat_id, text="На какое число хотите забронировать столик?",
                     reply_markup=rM)


def make_peoples_menu(bot, update):
    bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          text="Сколько человек придёт?")
    peoples_btns = []
    for i in range(21):
        if i == 0:
            i += 1
        peoples_btns.append(InlineKeyboardButton(text=i, callback_data=i + 33))
    bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=InlineKeyboardMarkup(build_menu(peoples_btns, n_cols=5)))


def book_confirmation(bot, update):
    if int(results.selected_day[update.callback_query.message.chat_id]) < now.day:
        selected_month = now.month + 1
    else:
        selected_month = now.month
    conf_text = "Проверь данные заявки 👇\n" \
                "Дата: {}.{}.{}\n" \
                "Время: {}\n" \
                "Людей: {}".format(results.selected_day[update.callback_query.message.chat_id], selected_month,
                                   now.year, results.selected_time[update.callback_query.message.chat_id],
                                   results.selected_people[update.callback_query.message.chat_id])
    bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          text=conf_text)
    rM = InlineKeyboardMarkup(build_menu([InlineKeyboardButton(text="Заказать", callback_data="order a table"),
                                          InlineKeyboardButton(text="Отменить", callback_data="cancel a table")], n_cols=2))
    bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=rM)
