from aiogram import Bot, Dispatcher, executor, types
from handlers.accent_handler import *


def k_button(text: str):
    return types.KeyboardButton(text=text)


def start_keyboard():
    kb = [
        [k_button('Ударения'), k_button('Задания')],
        [k_button('Cтатистика')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def accent_keyboard(user_id):
    if not check_id_in_list(user_id):
        create_new_words_for_user(user_id)
        words_user = get_words_user(user_id)
    else:
        words_user = get_words_user(user_id)
    words_user = ['хелло', 'бай']
    kb = [
        [k_button(words_user[0]), k_button(words_user[1])],
        [k_button('в главное меню')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
