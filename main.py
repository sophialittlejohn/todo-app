import sqlite3
from datetime import datetime, date

print(date.today())  # => 2018-06-22
print(datetime.now())  # => 2018-06-22 12:42:23.854477


class Database:
    def __init__(self):
        self.create_table()

    def create_table(self):
        sqlite_file = 'todo_db.sqlite'  # name of the sqlite database file

        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        # Creating a new SQLite table for countries
        try:
            c.execute('''
            CREATE TABLE todos (
              todo_id integer PRIMARY KEY,
              content text NOT NULL,
              created date
            );''')
        except sqlite3.OperationalError:
            print('DB already exists')

        # Committing changes and closing the connection to the database file
        conn.commit()
        conn.close()

