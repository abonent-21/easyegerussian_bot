import handlers.excel_handler
import sqlite3
import datetime
import db


class User:
    def __init__(self, user_id, chat_id, location='main_menu'):
        self.user_id = user_id
        self.chat_id = chat_id
        self.location = location
        self.subscription = {'status': False, 'time_exp': None}
        self.nums_of_current_tasks = db.get_from_db_current_num_of_user_task(user_id)
        self.task_1 = handlers.excel_handler.get_tasks_1_problems_from_excel()
        self.task_2 = None
        self.task_3 = None
        self.task_4 = handlers.excel_handler.get_tasks_4_problems_from_excel()
        self.task_3 = None
        self.all_tasks = [self.task_1, self.task_2, self.task_3, self.task_4]

    def get_user_location(self):
        return self.location

    def set_user_location(self, location: str):
        self.location = location

    def get_status_of_subscription(self):
        return self.subscription

    def set_subscription_status(self, status: bool, time_exp: str):
        self.subscription = {'status': status, 'time_exp': time_exp}

    def change_num_of_current_task_for_user(self, type_task: int, step: int):
        self.nums_of_current_tasks[f'task_{type_task}'] = \
            abs(self.nums_of_current_tasks[f'task_{type_task}'] + step) % len(self.all_tasks[type_task - 1])

    def check_correct_answer(self, type_task: int, input_word: str):
        if type_task == 1:
            input_word = input_word.strip().lower()
            return input_word in self.get_task_json(type_task=1)['correct_answers'].split()
        if type_task == 4:
            return input_word in self.get_task_json(type_task=4)['correct_word']

    def set_new_tasks_in_keyboard_for_user(self):
        self.task_1 = handlers.excel_handler.get_tasks_1_problems_from_excel()
        self.task_2 = None
        self.task_3 = None
        self.task_4 = handlers.excel_handler.get_tasks_4_problems_from_excel()
        self.all_tasks = [self.task_1, self.task_2, self.task_3, self.task_4]

    def give_task_for_user_in_text(self, type_task: int):
        if type_task == 1:
            task = self.get_task_json(type_task=type_task)
            num_in_column = task['num_in_column']
            description = task['description']
            text_of_task = task['text_of_task']
            text = 'Задание #' + num_in_column + "\n\n" + description \
                   + "\n\n" + text_of_task
            return text

    def save_all_current_data_in_db(self):
        connection = sqlite3.connect('handlers\\users_data\\current_users_data.db')
        cursor = connection.cursor()
        data = [self.user_id]
        for i in range(1, 27):
            data.append(self.nums_of_current_tasks[f'task_{i}'])
        data = tuple(data)
        qu = '?, ' * 26 + '?'
        cursor.execute('''
        INSERT or REPLACE  INTO users_location
                              (user_id, user_chat_id, location)
                              VALUES (?, ?, ?);
        ''', (self.user_id, self.chat_id, self.location))
        cursor.execute(f'''
                INSERT or REPLACE INTO  users_tasks VALUES ({qu});''', data)
        connection.commit()
        connection.close()

    def save_important_users_data_in_db(self):
        pass

    def get_user_chat_id(self):
        return self.chat_id

    def get_task_json(self, type_task: int):
        num_of_current_task = self.nums_of_current_tasks[f'task_{type_task}']
        task_json = self.all_tasks[type_task - 1][num_of_current_task]
        return task_json
