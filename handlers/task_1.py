import handlers.excel_handler

users_current_tasks = {}


def get_tasks_from_excel(num_of_task):
    return handlers.excel_handler.get_tasks_4_problems_from_excel()


def check_id_in_list_task_1(user_id):
    return user_id in users_current_task_1


