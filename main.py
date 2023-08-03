import logging
from config import config_bot
from aiogram import Bot, Dispatcher, executor, types
from keyborads import *
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config_bot.bot_token.get_secret_value())
dp = Dispatcher(bot)

users_location = {}


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    users_location[message.from_user.id] = 'main_menu'
    await message.answer("Привет, я бот для подготовки к ЕГЭ!",
                         reply_markup=start_keyboard())


@dp.message_handler(Text(equals='Ударения'))
async def accent(message: types.Message):
    users_location[message.from_user.id] = 'accent'
    await message.answer("Задание на ударение",
                         reply_markup=accent_keyboard(message.from_user.id))
@dp.message_handler(Text(equals='в главное меню'))
async def return_to_main_menu(message: types.Message):
    users_location[message.from_user.id] = 'main_menu'
    await message.answer("Вы в главном меню.",
                         reply_markup=start_keyboard())
@dp.message_handler(lambda message: users_location[message.from_user.id] == 'accent')
async def get_user_accent(message: types.Message):
    await message.answer("проверка слова",
                         reply_markup=accent_keyboard(message.from_user.id))





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
