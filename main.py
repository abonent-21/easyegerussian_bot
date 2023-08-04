import logging
from config import config_bot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import os
import datetime

from keyborads import *
from handlers.task_4_handler import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config_bot.bot_token.get_secret_value())
dp = Dispatcher(bot)

users_location = {}


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
@dp.message_handler(Text(equals='Ударения'))
async def accent(message: types.Message):
    users_location[message.from_user.id] = 'accent'
    await message.answer("Задание на ударение",
                         reply_markup=accent_keyboard(message.from_user.id))


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
    users_location[callback.from_user.id] = 'admin_edit_panel'
    num_of_task = callback.data.split('_')[-1]
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


@dp.message_handler(lambda message: message.text == 'Вернуться в меню админа 👈' and \
                                    users_location[message.from_user.id] in ['admin_menu', 'admin_edit_panel'])
async def return_to_admin_menu(message: types.Message):
    users_location[message.from_user.id] = 'admin_menu'
    await message.answer(f"Главное меню:",
                         reply_markup=start_admin_keybord())


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def fileHandle(message: types.Message):
    name, type_file = message.document.file_name.split('.')
    if users_location[message.from_user.id] == 'admin_edit_panel':
        await message.answer(f'Файл {name} отпрвлен на проверку, ждите подтверждение.')
        path = os.path.abspath('requests_to_edit_file')
        time = f'{datetime.datetime.now()}'
        idx = time.rfind('.')
        time = time[:idx].replace(':', '-')
        destination = path + rf"\{name} ({time})_({message.from_user.id}).{type_file}"
        print(destination)
        await message.document.download(destination_file=destination)
    else:
        await message.answer(f'Здесь нельзя отпрвить файл.')


# --------------------------------------------------------------------------------
@dp.message_handler(lambda message: users_location[message.from_user.id] == 'accent')
async def get_user_accent(message: types.Message):
    correct_word = users_current_accent_words[message.from_user.id]['correct_word']
    incorrect_word = users_current_accent_words[message.from_user.id]['incorrect_word']
    current_num = users_current_accent_words[message.from_user.id]['current_num']
    if message.text == correct_word:
        give_new_words_for_user(message.from_user.id, current_num)
        await message.answer("Верно!  ✅",
                             reply_markup=accent_keyboard(message.from_user.id))
    elif message.text == incorrect_word:
        await message.answer("Неверно =(   ❌",
                             reply_markup=start_keyboard())


# --------------------------------------------------------------------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
