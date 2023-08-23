import logging
from config import config_bot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import os
import datetime
import random
import shutil
import atexit

import users
from keyborads import *
import db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config_bot.bot_token.get_secret_value())
dp = Dispatcher(bot)

users_data = db.get_users_class_data_from_db()


# -----------------COMMANDS--------------------------------------------------------------

@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    users_data[message.from_user.id] = users.User(message.from_user.id, message.chat.id)
    await message.answer("Привет, я бот для подготовки к ЕГЭ!",
                         reply_markup=start_keyboard())


@dp.message_handler(commands='admin')
async def start_message(message: types.Message):
    users_data[message.from_user.id].set_user_location('admin_menu')
    users_data[message.from_user.id].set_subscription_status(status=True,time_start='inf', time_exp='inf')
    await message.answer("Добро пожаловать, мастер!", reply_markup=start_admin_keybord())


@dp.message_handler(commands='stop')
async def stop_message(message: types.Message):
    for user_id in users_data:
        users_data[user_id].save_all_current_data_in_db()
        await bot.send_message(chat_id=users_data[user_id].get_user_chat_id(),
                               text=f'Бот 🤖 ремонтируется ⚙️,\t'
                                    f'приносим свои извинения.'
                                    f'\nВаш прогресс сохранен 📝.')
        exit()


async def message_all_about_start(_):
    for user_id in users_data:
        await bot.send_message(chat_id=users_data[user_id].get_user_chat_id(),
                               text=f'Бот 🤖 cнова работает 🦾 !\nНажми --> /start')


# -----------------USER MENU-------------------------------------------------------------
# handler to user get to another handler
@dp.callback_query_handler(text_startswith='solve_task')
async def handler_for_users_task(callback: types.CallbackQuery):
    num_of_task = callback.data.split('_')[-1]
    if num_of_task == '1':
        users_data[callback.from_user.id].set_user_location('solve_task_1')
        await callback.message.answer("Задание №1:", reply_markup=back_to_start_keyboard())
        await callback.message.answer(users_data[callback.from_user.id].give_task_for_user_in_text(type_task=1))
        await callback.message.answer("Введите ответ:")
    if num_of_task == '4':
        users_data[callback.from_user.id].set_user_location('solve_task_4')
        await callback.message.answer("Задание №4:",
                                      reply_markup=task_4_keyboard(user=users_data[callback.from_user.id]))
    await callback.answer()


# button to show list of tasks
@dp.message_handler(Text(equals='Задания'))
async def list_of_tasks(message: types.Message):
    await message.answer("Список заданий:",
                         reply_markup=list_of_student_task())


@dp.message_handler(Text(equals='Доп. информация'))
async def list_of_tasks(message: types.Message):
    await message.answer("Дополнительная информация:",
                         reply_markup=additional_information())


@dp.message_handler(Text(equals='Подписка'))
async def price_of_sub(message: types.Message):
    await message.answer("Подписки:",
                         reply_markup=price_list_of_sub())


@dp.callback_query_handler(text_startswith='buy_sub')
async def price_of_sub(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, 'Подписки',
                           reply_markup=price_list_of_sub())
    await callback.answer()


@dp.message_handler(Text(equals='Статус подписки'))
async def price_of_sub(message: types.Message):
    sub_data = users_data[message.from_user.id].get_status_of_subscription()


# handler for inline button to switch task in user menu
@dp.callback_query_handler(text_startswith='kb_solve')
async def kb_solve(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=list_of_student_task(callback.data))
    await callback.answer()


# button to return in main user menu
@dp.message_handler(lambda message: message.text in ['Вернуться 👈', 'в главное меню'])
async def return_to_main_menu(message: types.Message):
    users_data[message.from_user.id].set_user_location('main_menu')
    await message.answer("Вы в главном меню.",
                         reply_markup=start_keyboard())


@dp.callback_query_handler(text_startswith='show_correct_answer')
async def show_correct_answer(callback: types.CallbackQuery):
    status_of_sub = users_data[callback.from_user.id].get_status_of_subscription()['status']
    time_of_exp = users_data[callback.from_user.id].get_status_of_subscription()['time_exp']
    type_and_num = callback.data.split()[-1].split('/')
    type_of_task = int(type_and_num[0])
    num_of_task = int(type_and_num[1])
    if status_of_sub:
        task = users_data[callback.from_user.id].get_dict_of_task(type_of_task, num_of_task)
        await callback.message.answer('<i><b>Пояснение:</b></i>', parse_mode="HTML")
        await callback.message.answer(task['explanation'])
        await callback.message.answer('<i><b>Видео:</b></i>', parse_mode="HTML")
        await callback.message.answer(task['video_with_explanation'])
        await callback.message.answer('Тайм код: ' + task['time_code_of_video'])
        await callback.message.answer('<i><b>Теория:</b></i>', parse_mode="HTML")
        await callback.message.answer(task['number_of_theory'])
    else:
        await callback.message.answer('У вас не активирована подписка. Нажми 👇, чтобы активировать',
                                      reply_markup=send_to_buy_sub())
    await callback.answer()
    await callback.message.edit_reply_markup()


# -----------------ADMIN MENU--------------------------------------------------------------

# button for admin to edit task file
@dp.message_handler(lambda message: message.text == 'Добавить задание' and \
                                    users_data[message.from_user.id].get_user_location() == 'admin_menu')
async def edit_students_task(message: types.Message):
    await message.answer("Вы в мастерской заданий.",
                         reply_markup=task_admin_keyboard())


# funcion give file for admin
@dp.callback_query_handler(text_startswith='edit_task')
async def edit_task_4(callback: types.CallbackQuery):
    num_of_task = callback.data.split('_')[-1]
    users_data[callback.from_user.id].set_user_location(f'admin_edit_panel_{num_of_task}')
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


# buttons to switch button for edit task
@dp.callback_query_handler(text_startswith='kb_edit')
async def change_edit_line(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=task_admin_keyboard(callback.data))
    await callback.answer()


# inline button for special chat to check files from admins
@dp.callback_query_handler(text_startswith='file')
async def allow_or_reject_file(callback: types.CallbackQuery):
    type_answer = callback.data.split('_')[-1]
    code_of_file = int(callback.message.text.split()[-4])
    chatid = int(callback.message.text.split()[-1])
    path = os.path.abspath('requests_to_edit_file')
    name_file = ''
    full_name_of_file = ''
    date = ''
    type_file = ''
    for file in os.listdir(path):
        if str(code_of_file) in file:
            full_name_of_file = file
            name_file = file[file.rfind(' ') + 1:].split('.')[0]
            type_file = file[file.rfind(' ') + 1:].split('.')[1]
            date = file[:file.find('_')].replace('(', '').replace(')', '')
            break
    if type_answer == 'allow':
        destination = os.path.abspath(f'handlers\\materials_for_studying\\{name_file}')
        shutil.copy(path + "\\" + full_name_of_file, destination)
        os.remove(path + "\\" + full_name_of_file)
        os.remove(destination + "\\" + name_file + '.' + type_file)
        old_file = os.path.join(destination, full_name_of_file)
        new_file = os.path.join(destination, name_file + '.' + type_file)
        os.rename(old_file, new_file)
        for user in users_data.values():
            user.set_new_tasks_in_keyboard_for_user()
        await bot.send_message(chat_id=chatid, text=f'Ваши изменения от {date} файла '
                                                    f'{name_file}.{type_file}  одобрены! ✅')
    elif type_answer == 'reject':
        await bot.send_message(chat_id=chatid, text='Ваши изменения отклонены ❌. '
                                                    'Причину напишут вам в личных сообщениях.')
        os.remove(path + '\\' + full_name_of_file)
    await callback.message.edit_reply_markup()
    await callback.answer()


# button to return in admin menu
@dp.message_handler(lambda message: message.text == 'Вернуться в меню админа 👈' \
                                    and 'admin' in users_data[message.from_user.id].get_user_location())
async def return_to_admin_menu(message: types.Message):
    users_data[message.from_user.id].set_user_location('admin_menu')
    await message.answer(f"Главное меню:",
                         reply_markup=start_admin_keybord())


# funcion to get and check file
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def fileHandle(message: types.Message):
    name, type_file = message.document.file_name.split('.')
    num_of_task = users_data[message.from_user.id].get_user_location().split('_')[-1]
    code = random.randint(1000000, 9999999)
    if 'admin_edit_panel' not in users_data[message.from_user.id].get_user_location():
        await message.answer(f'Здесь нельзя отправить файл.')
    elif type_file != 'xlsx' or f'task_{num_of_task}' != name:
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


# ---------------------CURRENT REQUESTS FROM USERS / HANDLERS FOR TASKS---------------------------------------------------------

@dp.message_handler(lambda message: users_data[message.from_user.id].get_user_location() == 'solve_task_1')
async def get_user_accent_task_1(message: types.Message):
    if users_data[message.from_user.id].check_correct_answer(type_task=1, input_word=message.text):
        users_data[message.from_user.id].change_num_of_current_task_for_user(type_task=1, step=1)
        await message.answer("Верно!  ✅")
        await message.answer(users_data[message.from_user.id].give_task_for_user_in_text(type_task=1))
        await message.answer("Введите ответ:")
    else:
        users_data[message.from_user.id].set_user_location('main_menu')
        await message.answer("Неверно =(   ❌",
                             reply_markup=start_keyboard())
        num = users_data[message.from_user.id].get_num_of_current_tasks(type=1)
        await message.answer("Посмотреть ответ 👇",
                             reply_markup=check_correct_answer(type_task=1, num_of_task=num))


# check current users answers for task 4
@dp.message_handler(lambda message: users_data[message.from_user.id].get_user_location() == 'solve_task_4')
async def get_user_accent_task_4(message: types.Message):
    if users_data[message.from_user.id].check_correct_answer(type_task=4, input_word=message.text):
        users_data[message.from_user.id].change_num_of_current_task_for_user(type_task=4, step=1)
        await message.answer("Верно!  ✅",
                             reply_markup=task_4_keyboard(user=users_data[message.from_user.id]))
    else:
        users_data[message.from_user.id].set_user_location('main_menu')
        await message.answer("Неверно =(   ❌",
                             reply_markup=start_keyboard())
        


# --------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=message_all_about_start)
    finally:
        for user_id in users_data:
            users_data[user_id].save_all_current_data_in_db()
