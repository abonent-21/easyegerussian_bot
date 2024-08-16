import sqlite3
import users
from pprint import pprint

def get_stat_from 

def get_users_class_data_from_db():
    conn = sqlite3.connect('handlers\\users_data\\current_users_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users_location""")
    data = cur.fetchall()
    users_dict = {}
    for user in data:
        user_id = user[0]
        chat_user_id = user[1]
        location = user[2]
        users_dict[user_id] = users.User(user_id=user_id, chat_id=chat_user_id, location=location)
    conn.commit()
    conn.close()
    return users_dict


def get_from_db_current_num_of_user_task(user_id: int):
    conn = sqlite3.connect('handlers\\users_data\\current_users_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users_tasks WHERE user_id = ?""", (user_id,))
    data = cur.fetchall()[0][1:]
    names_of_tasks = list(map(lambda x: x[0], cur.description))[1:]
    nums_of_current_tasks = {}
    if data:
        for idx in range(len(data)):
            nums_of_current_tasks[names_of_tasks[idx]] = data[idx]
    else:
        for i in range(1, 27):
            nums_of_current_tasks[f'task_{i}'] = 0
    conn.commit()
    conn.close()
    return nums_of_current_tasks


def get_from_db_status_of_subscription(user_id):
    conn = sqlite3.connect('handlers\\users_data\\users.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users_subscription WHERE user_id = ?""", (user_id,))
    data = cur.fetchall()[0][1:]
    names_of_tasks = list(map(lambda x: x[0], cur.description))[1:]
    subscription = {}
    if data:
        for idx in range(len(data)):
            subscription[names_of_tasks[idx]] = data[idx]
    else:
        subscription = {'status': False, 'time_start': None, 'time_exp': None}
    print(subscription)
    return subscription
