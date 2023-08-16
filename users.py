import handlers.excel_handler


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.location = 'main_menu'
        self.subscription = {'status': False, 'time_exp': None}
        self.nums_of_current_tasks = {}
        for i in range(1, 27):
            self.nums_of_current_tasks[f'task_{i}'] = 0
        self.task_1 = handlers.excel_handler.get_tasks_1_problems_from_excel()
        self.task_4 = handlers.excel_handler.get_tasks_4_problems_from_excel()

    def get_user_location(self):
        return self.location

    def set_user_location(self, location):
        self.location = location

    def get_status_of_subscription(self):
        return self.subscription

    def set_subscription_status(self, status: bool, time_exp: str):
        self.subscription = {'status': status, 'time_exp': time_exp}

    def give_new_task_for_user(self, type_task, step):
        self.nums_of_current_tasks[type_task] += step

    def check_correct_answers(self, type_task: int, input_word: str):
        if type_task == 4:
            return input_word == self.task_4['correct_word']

    def get_task(self, type_task: int):
        if type_task == 4:
            num_of_task = self.nums_of_current_tasks['task_4']
            return self.task_4[num_of_task]
