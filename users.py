import handlers.excel_handler
import sqlite3
import os
import db


class User:
    def __init__(self, user_id, user_login, location='main_menu'):
        self.user_id = user_id
        self.user_login = user_login
        self.location = location
        # self.subscription = db.get_from_db_status_of_subscription(user_id)
        self.subscription = {'status': True, 'time_start': 'inf', 'time_exp': 'inf'}
        self.nums_of_current_tasks = db.get_from_db_current_num_of_user_task(user_id)
        self.dict_of_tasks = {}
        for num_task in range(1, 26 + 1):
            self.dict_of_tasks[f'task_{num_task}'] = handlers.excel_handler.get_tasks_problems_from_excel(num_task)
        self.stat = self.get_user_stat()
        
    def get_user_id(self):
        return self.user_id

    def get_user_location(self):
        return self.location

    def get_dict_of_tasks(self, type_of_task, num):
        return self.dict_of_tasks[f'task_{type_of_task}'][num]

    def set_user_location(self, location: str):
        self.location = location

    def get_num_of_current_tasks(self, type_of_task: int):
        return self.nums_of_current_tasks[f'task_{type_of_task}']

    def get_status_of_subscription(self):
        return self.subscription

    def set_subscription_status(self, status: bool, time_start: str, time_exp: str):
        self.subscription = {'status': status, 'time_start': time_start, 'time_exp': time_exp}

    def change_num_of_current_task_for_user(self, type_task: int, step: int):
        self.nums_of_current_tasks[f'task_{type_task}'] = \
            abs(self.nums_of_current_tasks[f'task_{type_task}'] + step) % \
            len(self.dict_of_tasks[f'task_{type_task}'])

    def check_correct_answer(self, type_task: int, input_word: str):
        if type_task == 4:
            return input_word in self.get_task_json(type_task=4)['correct_word']
        else:
            input_word = input_word.strip().lower()
            return input_word in self.get_task_json(type_task=1)['correct_answers'].split()

    def get_user_stat(self):
        percent_of_completed_tasks = {}
        for task in self.nums_of_current_tasks:
            if len(self.dict_of_tasks[task]) != 0:
                percent = round(self.nums_of_current_tasks[task] / len(self.dict_of_tasks[task]), 2)
            else:
                percent = 0
            percent_of_completed_tasks[task] = percent * 100
        return percent_of_completed_tasks

    def give_task_for_user_in_text(self, type_task: int):
        task = self.get_task_json(type_task=type_task)
        num_in_column = task['num_in_column']
        description = task['description']
        text_of_task = task['text_of_task']
        text = 'Номер #' + num_in_column + "\n\n" + description + "\n\n" + text_of_task
        return text

    def set_new_tasks_in_keyboard_for_user(self):
        for num_task in range(1, 26 + 1):
            self.dict_of_tasks[f'task_{num_task}'] = handlers.excel_handler.get_tasks_problems_from_excel(num_task)


    def save_all_current_data_in_db(self):
        connection = sqlite3.connect('handlers/users_data/current_users_data.db', timeout=7)
        cursor = connection.cursor()
        data = [self.user_id]
        for i in range(1, 27):
            data.append(self.nums_of_current_tasks[f'task_{i}'])
        data = tuple(data)
        qu = '?, ' * 26 + '?'
        cursor.execute('''
        INSERT or REPLACE  INTO users_location
                              (user_id, user_login, location)
                              VALUES (?, ?, ?);
        ''', (self.user_id, self.user_login, self.location))
        cursor.execute(f'''
                INSERT or REPLACE INTO  users_tasks VALUES ({qu});''', data)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('handlers/users_data/users.db')
        cursor = connection.cursor()
        sub_data = self.get_status_of_subscription()
        status_subscription = sub_data['status']
        start_subscription = str(sub_data['time_start'])
        end_subscription = str(sub_data['time_exp'])
        cursor.execute('''
                INSERT or REPLACE  INTO users_subscription
                                      (user_id, status,
                                      time_start, time_exp)
                                      VALUES (?, ?, ?, ?);
                ''', (self.user_id,
                      status_subscription,
                      start_subscription,
                      end_subscription))
        connection.commit()
        connection.close()

    def save_important_users_data_in_db(self):
        pass

    def get_user_user_login(self):
        return self.chat_id

    def get_task_json(self, type_task: int):
        num_of_current_task = self.nums_of_current_tasks[f'task_{type_task}']
        task_json = self.dict_of_tasks[f'task_{type_task}'][num_of_current_task]
        return task_json
