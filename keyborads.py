from aiogram import types
from handlers.task_4_handler import *
from random import shuffle


def k_button(text: str):
    return types.KeyboardButton(text=text)




# ////////////////////////////////////////////////////////////////////////////////////////
def start_keyboard():
    kb = [
        [k_button('Ударения'), k_button('Задания')],
        [k_button('Cтатистика')], [k_button('Теория')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def accent_keyboard(user_id):
    if not check_id_in_list(user_id):
        create_new_words_for_new_user(user_id)
        words_user = get_words_user(user_id)
    else:
        words_user = get_words_user(user_id)
    shuffle(words_user)
    kb = [
        [k_button(words_user[0]), k_button(words_user[1])],
        [k_button('в главное меню')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


# ////////////////////////////////////////////////////////////////////////////////////////

def start_admin_keybord():
    kb = [[k_button('Добавить задание'), k_button('Забанить'), k_button('Объявления')],
          [k_button('Вернуться 👈')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def task_admin_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 27):
        kb.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}'))
    return kb


def back_to_admin_menu():
    kb = [[k_button('Вернуться в меню админа 👈')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


