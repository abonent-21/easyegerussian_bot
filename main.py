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

USERS_DATA = db.get_users_class_data_from_db()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config_bot.bot_token.get_secret_value())
dp = Dispatcher(bot)
# -----------------COMMANDS--------------------------------------------------------------

@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    USERS_DATA[message.from_user.id] = users.User(message.from_user.id, message.from_user.username)
    print(USERS_DATA)
    await message.answer("Привет, я бот для подготовки к ЕГЭ! (бета версия)\n\n возникли ошибки, вопросы пиши --> @G30rG32",
                         reply_markup=start_keyboard())


@dp.message_handler(commands='admin1232!')
async def admin_menu(message: types.Message):
    USERS_DATA[message.from_user.id].set_user_location('admin_menu')
    USERS_DATA[message.from_user.id].set_subscription_status(status=True,time_start='inf', time_exp='inf')
    await message.answer("Добро пожаловать, мастер!", reply_markup=start_admin_keybord())

@dp.message_handler(commands='stat')
async def stat_of_users(message: types.Message):
    info = db.get_login_of_users()
    text = ''
    for user in info:
        text += f'@{user}\n'
    await message.answer(text)
    await message.answer(f"Всего пользователей: {len(info)}")

@dp.message_handler(Text(equals='Статистика'))
async def stat_of_users(message: types.Message):
    text = ''
    user_id = message.from_user.id
    stat = USERS_DATA[user_id].get_user_stat()
    all_info = ""
    for task in range(1, 27):
        text = f'Задание {task}'
        percent = stat[f'task_{task}']
        count_green_squars = int(percent // 10)
        text_stat = "🟩" * count_green_squars + "⬜" * (10 - count_green_squars)
        text_stat += f" {percent}%"
        all_info += text + '\n' + text_stat + '\n\n'
    await message.answer(all_info)


@dp.message_handler(commands='save')
async def save_all_data(message: types.Message):
    for user_id in USERS_DATA:
        USERS_DATA[user_id].save_all_current_data_in_db()
    await message.answer("Данные сохранены")

@dp.message_handler(commands='stop3391')
async def stop_message(message: types.Message):
    for user_id in USERS_DATA:
        USERS_DATA[user_id].save_all_current_data_in_db()
        await bot.send_message(chat_id=USERS_DATA[user_id].get_user_chat_id(),
                               text=f'Бот 🤖 ремонтируется ⚙️,\t'
                                    f'приносим свои извинения.'
                                    f'\nВаш прогресс сохранен 📝.')
        exit()


async def message_all_about_start(_):
        for user_id in USERS_DATA:
            try:
                await bot.send_message(chat_id=USERS_DATA[user_id].get_user_id(),
                                    text=f'Бот 🤖 cнова работает 🦾 !\nНажми --> /start')
            except Exception as ex:
                print('Ошибка в отправке сообщения user')

# -----------------USER MENU-------------------------------------------------------------
# handler to user get to another handler
@dp.callback_query_handler(text_startswith='solve_task')
async def handler_for_users_task(callback: types.CallbackQuery):
    num_of_task = callback.data.split('_')[-1]
    print(num_of_task)
    if num_of_task != '4':
        USERS_DATA[callback.from_user.id].set_user_location(f'solve_task_{num_of_task}')
        await callback.message.answer(f"Задание №{num_of_task}:", reply_markup=back_to_start_keyboard())
        await callback.message.answer(USERS_DATA[callback.from_user.id].give_task_for_user_in_text(
            type_task=int(num_of_task)))
        await callback.message.answer("Введите ответ:")
    if num_of_task == '4':
        USERS_DATA[callback.from_user.id].set_user_location('solve_task_4')
        await callback.message.answer("Задание №4:",
                                      reply_markup=task_4_keyboard(user=USERS_DATA[callback.from_user.id]))
    await callback.answer()


# button to show list of tasks
@dp.message_handler(Text(equals='Задания'))
async def list_of_tasks(message: types.Message):
    await message.answer("Список заданий:",
                         reply_markup=list_of_student_task())

@dp.message_handler(Text(equals='Теория'))
async def list_of_tasks(message: types.Message):
    with open('handlers/materials_for_studying/theory/theory.txt') as target:
        text = ''.join(target.readlines())
        await message.answer(text)

@dp.message_handler(Text(equals='Доп. информация'))
async def list_of_tasks(message: types.Message):
    await message.answer("Дополнительная информация:",
                         reply_markup=additional_information())


@dp.message_handler(Text(equals='Подписка'))
async def price_of_sub(message: types.Message):
    await message.answer("Подписки:",
                         reply_markup=price_list_of_sub())
    INFO = "На данный момент бот дорабатывается, и подписка у всех активна\.\n"
    INFO += "Вы можете задонатить любую сумму на этот счет `2200700858400814`\n"
    INFO += "и взамен *получите активную подписку* на год, когда платные подписки вступят в силу\n"
    INFO += "\(в сообщении укажите свой @логин телеграмм\)"
    await message.answer(INFO, parse_mode="MarkdownV2")


@dp.callback_query_handler(text_startswith='buy_sub')
async def price_of_sub(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, 'Подписки:',
                           reply_markup=price_list_of_sub())
    await callback.answer()


@dp.message_handler(Text(equals='Статус подписки'))
async def price_of_sub(message: types.Message):
    sub_data = USERS_DATA[message.from_user.id].get_status_of_subscription()
    INFO = f"<b>Статус</b>: {('Не активна ❌', 'Активна ✅')[sub_data['status']]}\n"
    INFO += f"<b>Начало</b>: {sub_data['time_start']} ⏳\n<b>Конец</b>: {sub_data['time_exp']} ⌛"
    await message.answer(INFO, parse_mode='HTML')

# handler for inline button to switch task in user menu
@dp.callback_query_handler(text_startswith='kb_solve')
async def kb_solve(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=list_of_student_task(callback.data))
    await callback.answer()


# button to return in main user menu
@dp.message_handler(lambda message: message.text in ['Вернуться 👈', 'в главное меню'])
async def return_to_main_menu(message: types.Message):
    USERS_DATA[message.from_user.id].set_user_location('main_menu')
    await message.answer("Вы в главном меню.",
                         reply_markup=start_keyboard())


@dp.callback_query_handler(text_startswith='show_correct_answer')
async def show_correct_answer(callback: types.CallbackQuery):
    status_of_sub = USERS_DATA[callback.from_user.id].get_status_of_subscription()['status']
    time_of_exp = USERS_DATA[callback.from_user.id].get_status_of_subscription()['time_exp']
    type_and_num = callback.data.split()[-1].split('/')
    type_of_task = int(type_and_num[0])
    num_of_task = int(type_and_num[1])
    if status_of_sub:
        task = USERS_DATA[callback.from_user.id].get_dict_of_tasks(type_of_task, num_of_task)
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
@dp.message_handler(lambda message: message.text == 'Добавить файл' and \
                                    USERS_DATA[message.from_user.id].get_user_location() == 'admin_menu')
async def edit_students_task(message: types.Message):
    await message.answer("Вы в мастерской заданий.",
                         reply_markup=task_admin_keyboard())

# funcion give file for admin
@dp.callback_query_handler(text_startswith='edit')
async def edit_tasks(callback: types.CallbackQuery):
    data = callback.data #edit_task_{num}.xlsx
    name_file = data[data.find('_') + 1:]
    name_folder = name_file[:name_file.find('.')]
    USERS_DATA[callback.from_user.id].set_user_location(f'admin_edit_panel_{name_folder}')
    path = f'handlers/materials_for_studying/{name_folder}/{name_file}'
    await callback.message.answer("Файл с заданиями:", reply_markup=back_to_admin_menu())
    if os.path.exists(path):
        try:
            with open(path, 'rb') as file:
                await callback.message.answer_document(file)
            await callback.message.answer("После редактирования отправте файл сюда 👇")
        except Exception as ex:
            await callback.message.answer(f"Ошибка: {ex}. Нажмите еще раз на кнопку")
            with open(path, 'w+') as file:
                file.write(' ')

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
        destination = os.path.abspath(f'handlers/materials_for_studying/{name_file}')
        shutil.copy(path + "/" + full_name_of_file, destination)
        os.remove(path + "/" + full_name_of_file)
        os.remove(destination + "/" + name_file + '.' + type_file)
        old_file = os.path.join(destination, full_name_of_file)
        new_file = os.path.join(destination, name_file + '.' + type_file)
        os.rename(old_file, new_file)
        for user in USERS_DATA.values():
            user.set_new_tasks_in_keyboard_for_user()
        await bot.send_message(chat_id=chatid, text=f'Ваши изменения от {date} файла '
                                                    f'{name_file}.{type_file}  одобрены! ✅')
    elif type_answer == 'reject':
        await bot.send_message(chat_id=chatid, text='Ваши изменения отклонены ❌. '
                                                    'Причину напишут вам в личных сообщениях.')
        os.remove(path + '/' + full_name_of_file)
    await callback.message.edit_reply_markup()
    await callback.answer()


# button to return in admin menu
@dp.message_handler(lambda message: message.text == 'Вернуться в меню админа 👈' \
                                    and 'admin' in USERS_DATA[message.from_user.id].get_user_location())
async def return_to_admin_menu(message: types.Message):
    USERS_DATA[message.from_user.id].set_user_location('admin_menu')
    await message.answer(f"Главное меню:",
                         reply_markup=start_admin_keybord())


# funcion to get and check file
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def fileHandle(message: types.Message):
    name_type_file =  message.document.file_name
    name = message.document.file_name.split('.')
    num_of_task = USERS_DATA[message.from_user.id].get_user_location().split('_')[-1]
    allow_files = [f'task_{num_of_task}.xlsx', 'theory.txt']
    code = random.randint(10000000, 99999999)
    if 'admin_edit_panel' not in USERS_DATA[message.from_user.id].get_user_location():
        await message.answer(f'Здесь нельзя отправить файл.')
    elif name_type_file not in allow_files:
        await message.answer(f'Файл должен иметь то же название и тип.')
    elif message.caption:
        await message.answer(f'Файл {name_type_file} отправлен на проверку, ждите подтверждение.')
        await bot.send_message(chat_id=-1001945133738,
                               text=message.caption + f'\n\nАдминистратор: @{message.from_user.username}\n'
                                                      f'Код файла: {code}\n' +
                                    f'Код чата: {message.from_user.id}',
                               reply_markup=yes_or_no_edit_file())
        path = os.path.abspath('requests_to_edit_file')
        time = f'{datetime.datetime.now()}'
        idx = time.rfind('.')
        time = time[:idx].replace(':', '-')
        destination = path + rf"/({time})_({code}) {name_type_file}"
        await message.document.download(destination_file=destination)
        file = [f for f in os.listdir(path)][-1]
        with open(path + "/" + file, 'rb') as f:
            await bot.send_document(chat_id=-1001945133738, document=f)
    elif not message.caption:
        await message.answer(f'Необходимо описать изменения файла.')


# ---------------------CURRENT REQUESTS FROM USERS / HANDLERS FOR TASKS---------------------------------------------------------

# check current users answers for task 4
@dp.message_handler(lambda message: USERS_DATA[message.from_user.id].get_user_location() == 'solve_task_4')
async def check_user_task_4_keyboard(message: types.Message):
    if USERS_DATA[message.from_user.id].check_correct_answer(type_task=4, input_word=message.text):
        USERS_DATA[message.from_user.id].change_num_of_current_task_for_user(type_task=4, step=1)
        await message.answer("Верно! ✅",
                             reply_markup=task_4_keyboard(user=USERS_DATA[message.from_user.id]))
    else:
        USERS_DATA[message.from_user.id].set_user_location('main_menu')
        await message.answer("Неверно =( ❌",
                             reply_markup=start_keyboard())

@dp.message_handler(lambda message: 'solve_task' in USERS_DATA[message.from_user.id].get_user_location())
async def check_user_tasks_keyboard(message: types.Message):
    task = int(USERS_DATA[message.from_user.id].get_user_location().split('_')[-1])
    if USERS_DATA[message.from_user.id].check_correct_answer(type_task=task, input_word=message.text):
        USERS_DATA[message.from_user.id].change_num_of_current_task_for_user(type_task=task, step=1)
        await message.answer("Верно! ✅")
        await message.answer(USERS_DATA[message.from_user.id].give_task_for_user_in_text(type_task=task))
        await message.answer("Введите ответ:")
    else:
        USERS_DATA[message.from_user.id].set_user_location('main_menu')
        await message.answer("Неверно =( ❌",
                             reply_markup=start_keyboard())
        num = USERS_DATA[message.from_user.id].get_num_of_current_tasks(type_of_task=task)
        await message.answer("Посмотреть ответ 👇",
                             reply_markup=check_correct_answer(type_task=task, num_of_task=num))




# --------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=message_all_about_start)
    finally:
        print("Бот отключен")
