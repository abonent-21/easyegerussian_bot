import sqlite3
import handlers.task_4_handler




def get_users_location():
    conn = sqlite3.connect('handlers\\users_data\\current_users_data.db')
    cur = conn.cursor()
    users_location = {}
    cur.execute("""SELECT * FROM users_location""")
    data = cur.fetchall()
    for i in data:
        users_location[i[0]] = i[1]
    return users_location
