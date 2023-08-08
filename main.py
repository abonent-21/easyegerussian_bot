import logging
from config import config_bot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import os
import datetime
import sqlite3
import random
import shutil

from keyborads import *
from handlers.task_4_handler import *
import db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config_bot.bot_token.get_secret_value())
dp = Dispatcher(bot)

users_location = db.get_users_location()


# ----------------------------------------------------------------------------------

@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    users_location[message.from_user.id] = 'main_menu'
    await message.answer("Привет, я бот для подготовки к ЕГЭ!",
                         reply_markup=start_keyboard())


@dp.message_handler(commands='admin')
async def start_message(message: types.Message):
    users_location[message.from_user.id] = 'admin_menu'
    await message.answer("Добро пожаловать, мастер!", reply_markup=start_admin_keybord())


# --------------------------------------------------------------------------------
@dp.callback_query_handler(text_startswith='solve_task')
async def accent(callback: types.CallbackQuery):
    num_of_task = callback.data.split('_')[-1]
    if num_of_task == '4':
        users_location[callback.from_user.id] = 'accent'
        await callback.message.answer("Задание на ударение:",
                                      reply_markup=task_4_keyboard(callback.from_user.id))
    await callback.answer()


@dp.message_handler(Text(equals='Задания'))
async def accent(message: types.Message):
    await message.answer("Список заданий:",
                         reply_markup=list_of_student_task())


@dp.callback_query_handler(text_startswith='kb_solve')
async def kb_solve(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=list_of_student_task(callback.data))


@dp.message_handler(lambda message: message.text in ['Вернуться 👈', 'в главное меню'])
async def return_to_main_menu(message: types.Message):
    users_location[message.from_user.id] = 'main_menu'
    await message.answer("Вы в главном меню.",
                         reply_markup=start_keyboard())


# --------------------------------------------------------------------------------

@dp.message_handler(lambda message: message.text == 'Добавить задание' and \
                                    users_location[message.from_user.id] == 'admin_menu')
async def edit_sutents_task(message: types.Message):
    await message.answer("Вы в мастерской заданий.",
                         reply_markup=task_admin_keyboard())


@dp.callback_query_handler(text_startswith='edit_task')
async def edit_task_4(callback: types.CallbackQuery):
    num_of_task = callback.data.split('_')[-1]
    users_location[callback.from_user.id] = f'admin_edit_panel_{num_of_task}'
    path = f'handlers/materials_for_studying/task_{num_of_task}/task_{num_of_task}.xlsx'
    await callback.message.answer("Файл с заданиями:", reply_markup=back_to_admin_menu())
    if os.path.exists(path):
        with open(path, 'rb') as file:
            await callback.message.answer_document(file)
        await callback.message.answer("После редактирования отправте файл сюда 👇")
    else:
        await callback.message.answer("*файл отсутствует*")
        await callback.message.answer("Новый файл можно отправить сюда 👇")
    await callback.answer()


# ДЛЯ ПРОЛИСТЫВАНИЯ ЗАДАНИЙ У АДМИНА
@dp.callback_query_handler(text_startswith='kb_edit')
async def change_edit_line(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=task_admin_keyboard(callback.data))


@dp.callback_query_handler(text_startswith='file')
async def allow_or_reject_file(callback: types.CallbackQuery):
    type_answer = callback.data.split('_')[-1]
    message_code = int(callback.message.text.split()[-4])
    chatid = int(callback.message.text.split()[-1])
    if type_answer == 'allow':
        path = os.path.abspath('requests_to_edit_file')
        name_file = ''
        full_name_file = ''
        date = ''
        type_file = ''
        for file in os.listdir(path):
            if str(message_code) in file:
                full_name_file = file
                name_file = file[file.rfind(' ') + 1:].split('.')[0]
                type_file = file[file.rfind(' ') + 1:].split('.')[1]
                date = file[:file.find('_')].replace('(', '').replace(')', '')
                break
        destination = os.path.abspath(f'handlers\\materials_for_studying\\{name_file}')
        shutil.copy(path + "\\" + full_name_file, destination)
        os.remove(path + "\\" + full_name_file)
        os.remove(destination + "\\" + name_file + '.' + type_file)
        old_file = os.path.join(destination, full_name_file)
        new_file = os.path.join(destination, name_file + '.' + type_file)
        os.rename(old_file, new_file)
        await bot.send_message(chat_id=chatid, text=f'Ваши изменения от {date} файла '
                                                    f'{name_file}.{type_file}  одобрены! ✅')
    elif type_answer == 'reject':
        await bot.send_message(chat_id=chatid, text='Ваши изменения отклонены ❌')
    await callback.message.edit_reply_markup()
    await callback.answer()


@dp.message_handler(lambda message: message.text == 'Вернуться в меню админа 👈' and \
                                    'admin' in users_location[message.from_user.id])
async def return_to_admin_menu(message: types.Message):
    users_location[message.from_user.id] = 'admin_menu'
    await message.answer(f"Главное меню:",
                         reply_markup=start_admin_keybord())


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def fileHandle(message: types.Message):
    name, type_file = message.document.file_name.split('.')
    num_of_task = users_location[message.from_user.id].split('_')[-1]
    code = random.randint(100000, 999999)
    if type_file != 'xlsx' or f'task_{num_of_task}' != name:
        await message.answer(f'Файл должен иметь то же название и тип.')
    elif message.caption:
        await message.answer(f'Файл {name}.{type_file} отпрвлен на проверку, ждите подтверждение.')
        await bot.send_message(chat_id=-1001945133738,
                               text=message.caption + f'\n\nАдминистратор: @{message.from_user.username}\n'
                                                      f'Код файла: {code}\n' +
                               f'Код чата: {message.from_user.id}',
                               reply_markup=yes_or_no_edit_file())
        path = os.path.abspath('requests_to_edit_file')
        time = f'{datetime.datetime.now()}'
        idx = time.rfind('.')
        time = time[:idx].replace(':', '-')
        destination = path + rf"\({time})_({code}) {name}.{type_file}"
        await message.document.download(destination_file=destination)
        file = [f for f in os.listdir(path)][-1]
        with open(path + "\\" + file, 'rb') as f:
            await bot.send_document(chat_id=-1001945133738, document=f)
    elif not message.caption:
        await message.answer(f'Необходимо описать изменения файла.')
    else:
        await message.answer(f'Здесь нельзя отпрвить файл.')


# --------------------------------------------------------------------------------
@dp.message_handler(lambda message: users_location[message.from_user.id] == 'accent')
async def get_user_accent(message: types.Message):
    correct_word = users_current_task_4_words[message.from_user.id]['correct_word']
    incorrect_word = users_current_task_4_words[message.from_user.id]['incorrect_word']
    current_num = users_current_task_4_words[message.from_user.id]['current_num']
    if message.text == correct_word:
        give_new_words_for_user(message.from_user.id, current_num)
        await message.answer("Верно!  ✅",
                             reply_markup=task_4_keyboard(message.from_user.id))
    elif message.text == incorrect_word:
        await message.answer("Неверно =(   ❌",
                             reply_markup=start_keyboard())


# --------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        conn = sqlite3.connect('handlers\\users_data\\current_users_data.db')
        cur = conn.cursor()
        users_id = [i for i in db.get_users_location()]
        for us in users_location:
            if us in users_id:
                cur.execute("update users_location set location=? where user_id=?", (users_location[us], us))
            else:
                cur.execute("INSERT INTO users_location (user_id, location) VALUES(?, ?);", (us, users_location[us]))
        conn.commit()
