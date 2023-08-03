import logging
from config import config_bot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from keyborads import *
from handlers.accent_handler import *

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


@dp.message_handler(lambda message: message.text in ['Вернуться 👈', 'В главное меню'])
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

@dp.message_handler(lambda message: message.text == 'Добавить задание/изменить 4' and \
                                    users_location[message.from_user.id] == 'admin_menu')
async def edit_task_4(message: types.Message):
    text = """"""
    with open("materials_for_studing/accents.json", encoding='UTF-8') as f:
        accents = json.load(f)
        counter = 0
        for words in accents:
            text += (f"{counter + 1}) Верное слово: {words['correct word']}\n"
                     f"Неверное: {words['incorrect word']}\n")
            counter += 1
    await message.answer(f"Список ударений: \n{text}",
                         reply_markup=back_to_admin_menu())

@dp.message_handler(lambda message: message.text == 'Вернуться в меню админа 👈' and \
                                    users_location[message.from_user.id] == 'admin_menu')
async def return_to_admin_menu(message: types.Message):
    await message.answer(f"Главное меню:",
                         reply_markup=start_admin_keybord())

# --------------------------------------------------------------------------------
@dp.message_handler(lambda message: users_location[message.from_user.id] == 'accent')
async def get_user_accent(message: types.Message):
    correct_word = users_words[message.from_user.id]['correct_word']
    current_num = users_words[message.from_user.id]['current_num']
    if message.text == correct_word:
        give_new_words_for_user(message.from_user.id, current_num)
        await message.answer("Верно!  ✅",
                             reply_markup=accent_keyboard(message.from_user.id))
    else:
        await message.answer("Неверно =(   ❌",
                             reply_markup=start_keyboard())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
