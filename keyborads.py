from aiogram import types
from users import User
from random import shuffle


def k_button(text: str):
    return types.KeyboardButton(text=text)


# ///////////////////////////////////USERS KEYBOARDS/////////////////////////////////////////////////////
def start_keyboard():
    kb = [
        [k_button('Задания')],
        [k_button('Теория')], [k_button('Доп. информация')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def additional_information():
    kb = [
        [k_button('Статистика')],
        [k_button('Подписка'), k_button('Статус подписки')],
        [k_button('Вернуться 👈')]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def price_list_of_sub():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(text=f'На 3 дня (бесплатно)',
                                      callback_data=f'subscription_trial'))
    kb.add(types.InlineKeyboardButton(text=f'На неделю  49 р',
                                      callback_data=f'subscription_week') )
    kb.add(types.InlineKeyboardButton(text=f'На месяц   139 р',
                                      callback_data=f'subscription_month'))
    kb.add(types.InlineKeyboardButton(text=f'На полгода 499 р',
                                      callback_data=f'subscription_half_year'))
    kb.add(types.InlineKeyboardButton(text=f'На год     599 р',
                                      callback_data=f'subscription_year'))
    return kb


def check_correct_answer(type_task, num_of_task):
    kb = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
    kb.add(types.InlineKeyboardButton(text=f'Пояснение',
                                      callback_data=f'show_correct_answer {type_task}/{num_of_task}'))
    return kb


def send_to_buy_sub():
    kb = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
    kb.add(types.InlineKeyboardButton(text=f'Активировать подписку 💸',
                                      callback_data=f'buy_sub'))
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


def list_of_student_task(type_kb='kb_solve_1_6'):
    kb_1_6 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6 + 1):
        kb_1_6.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_1_6.row(types.InlineKeyboardButton(text='➡️', callback_data='kb_solve_7_12'))

    kb_7_12 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(7, 12 + 1):
        kb_7_12.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_7_12.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_solve_1_6'),
                types.InlineKeyboardButton(text='➡️', callback_data='kb_solve_13_18'))

    kb_13_18 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(13, 18 + 1):
        kb_13_18.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_13_18.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_solve_7_12'),
                 types.InlineKeyboardButton(text='➡️', callback_data='kb_solve_19_26'))

    kb_19_26 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(19, 26 + 1):
        kb_19_26.add(types.InlineKeyboardButton(text=f'Задание {i}', callback_data=f'solve_task_{i}'))
    kb_19_26.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_solve_13_18'))

    if type_kb == "kb_solve_1_6":
        return kb_1_6
    elif type_kb == "kb_solve_7_12":
        return kb_7_12
    elif type_kb == "kb_solve_13_18":
        return kb_13_18
    elif type_kb == "kb_solve_19_26":
        return kb_19_26


# /////////////////////////////////ADMIN KEYBOARDS///////////////////////////////////////////////////////

def start_admin_keybord():
    kb = [[k_button('Добавить файл'),
            k_button('Забанить'),
            k_button('Объявления')],
            ['Вернуться 👈']]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def task_admin_keyboard(type_kb='kb_edit_1_6'):
    kb_1_6 = types.InlineKeyboardMarkup(row_width=1)
    kb_1_6.add(types.InlineKeyboardButton(text=f'Добавить/изменить теорию', callback_data=f'edit_theory.txt'))
    for i in range(1, 6 + 1):
        kb_1_6.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}.xlsx'))
    kb_1_6.row(types.InlineKeyboardButton(text='➡️', callback_data='kb_edit_7_12'))

    kb_7_12 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(7, 12 + 1):
        kb_7_12.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}.xlsx'))
    kb_7_12.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_edit_1_6'),
                types.InlineKeyboardButton(text='➡️', callback_data='kb_edit_13_18'))

    kb_13_18 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(13, 18 + 1):
        kb_13_18.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}.xlsx'))
    kb_13_18.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_edit_7_12'),
                 types.InlineKeyboardButton(text='➡️', callback_data='kb_edit_19_26'))

    kb_19_26 = types.InlineKeyboardMarkup(row_width=1)
    for i in range(19, 26 + 1):
        kb_19_26.add(types.InlineKeyboardButton(text=f'Добавить/изменить задание {i}', callback_data=f'edit_task_{i}.xlsx'))
    kb_19_26.row(types.InlineKeyboardButton(text='⬅️', callback_data='kb_edit_13_18'))

    if type_kb == "kb_edit_1_6":
        return kb_1_6
    elif type_kb == "kb_edit_7_12":
        return kb_7_12
    elif type_kb == "kb_edit_13_18":
        return kb_13_18
    elif type_kb == "kb_edit_19_26":
        return kb_19_26


def yes_or_no_edit_file():
    kb = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    kb.add(types.InlineKeyboardButton(text=f'Да', callback_data=f'file_allow'),
           types.InlineKeyboardButton(text=f'Нет', callback_data=f'file_reject'))
    return kb


def back_to_admin_menu():
    kb = [[k_button('Вернуться в меню админа 👈')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
