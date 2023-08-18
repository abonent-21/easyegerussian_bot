from aiogram import types
from users import User
from random import shuffle


def k_button(text: str):
    return types.KeyboardButton(text=text)


# ////////////////////////////////////////////////////////////////////////////////////////
def start_keyboard():
    kb = [
        [k_button('Задания')],
        [k_button('Cтатистика')], [k_button('Теория')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

def check_correct_answer():
    kb = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
    kb.add(types.InlineKeyboardButton(text=f'Посмотреть пояснение ', callback_data=f'show_correct_answer'))
    return kb


def back_to_start_keyboard():
    kb = [
        ['Вернуться 👈'],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def task_4_keyboard(user: User):
    task_4 = user.get_task_json(type_task=4)
    words_user = [task_4['correct_word'], task_4['incorrect_word']]
    shuffle(words_user)
    kb = [
        [k_button(words_user[0]), k_button(words_user[1])],
        [k_button('в главное меню')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def list_of_student_task(type_kb='kb_solve_1_5'):
    kb_1_5 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        kb_1_5.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_1_5.row(types.InlineKeyboardButton(text='➡️', callback_data='kb_solve_6_11'))

    kb_6_11 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(6, 12):
        kb_6_11.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_6_11.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_solve_1_5'),
                types.InlineKeyboardButton(text='➡️', callback_data='kb_solve_16_21'))

    kb_16_21 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(16, 22):
        kb_16_21.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_16_21.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_solve_6_11'),
                 types.InlineKeyboardButton(text='➡️', callback_data='kb_solve_22_26'))

    kb_22_26 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(22, 27):
        kb_22_26.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_22_26.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_solve_16_21'))

    if type_kb == "kb_solve_1_5":
        return kb_1_5
    elif type_kb == "kb_solve_6_11":
        return kb_6_11
    elif type_kb == "kb_solve_16_21":
        return kb_16_21
    elif type_kb == "kb_solve_22_26":
        return kb_22_26


# ////////////////////////////////////////////////////////////////////////////////////////

def start_admin_keybord():
    kb = [[k_button('Добавить задание'), k_button('Забанить'), k_button('Объявления')],
          [k_button('Вернуться 👈')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def task_admin_keyboard(type_kb='kb_edit_1_5'):
    kb_1_5 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        kb_1_5.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}'))
    kb_1_5.row(types.InlineKeyboardButton(text='➡️', callback_data='kb_edit_6_11'))

    kb_6_11 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(6, 12):
        kb_6_11.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}'))
    kb_6_11.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_edit_1_5'),
                types.InlineKeyboardButton(text='➡️', callback_data='kb_edit_16_21'))

    kb_16_21 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(16, 22):
        kb_16_21.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}'))
    kb_16_21.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_edit_6_11'),
                 types.InlineKeyboardButton(text='➡️', callback_data='kb_edit_22_26'))

    kb_22_26 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(22, 27):
        kb_22_26.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}'))
    kb_22_26.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_edit_16_21'))

    if type_kb == "kb_edit_1_5":
        return kb_1_5
    elif type_kb == "kb_edit_6_11":
        return kb_6_11
    elif type_kb == "kb_edit_16_21":
        return kb_16_21
    elif type_kb == "kb_edit_22_26":
        return kb_22_26


def yes_or_no_edit_file():
    kb = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    kb.add(types.InlineKeyboardButton(text=f'Да', callback_data=f'file_allow'),
           types.InlineKeyboardButton(text=f'Нет', callback_data=f'file_reject'))
    return kb


def back_to_admin_menu():
    kb = [[k_button('Вернуться в меню админа 👈')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
