import sqlite3

db = sqlite3.connect('handlers\\users_data\\users.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users_solved_task (
  user_id INTEGER,
  task_1 INTEGER,
  task_2 INTEGER,
  task_3 INTEGER,
  task_4 INTEGER,
  task_5 INTEGER,
  task_6 INTEGER,
  task_7 INTEGER,
  task_8 INTEGER,
  task_9 INTEGER,
  task_10 INTEGER,
  task_11 INTEGER,
  task_12 INTEGER,
  task_13 INTEGER,
  task_14 INTEGER,
  task_15 INTEGER,
  task_16 INTEGER,
  task_17 INTEGER,
  task_18 INTEGER,
  task_19 INTEGER,
  task_20 INTEGER,
  task_21 INTEGER,
  task_22 INTEGER,
  task_23 INTEGER,
  task_24 INTEGER,
  task_25 INTEGER,
  task_26 INTEGER
)""")

db.commit()
