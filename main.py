import sqlite3
from datetime import datetime, date

print(date.today())  # => 2018-06-22
print(datetime.now())  # => 2018-06-22 12:42:23.854477


class TODOApp:
    def __init__(self):
        self.create_table()

    def start(self):
        self.help_menu()

    def help_menu(self):
        print('''
        Help Menu:
        -------------------------
        'a' to add a todo
        'l' to list all todos
        'd' to delete a todo
        's' to search all todos
        'q' to quit
        ''')
        choice = input(' > ')
        if choice == 'a':
            return self.add_todo()
        elif choice == 'l':
            self.list_all_todos()
        elif choice == 'd':
            return self.remove_todo()
        elif choice == 's':
            return self.search_todos()
        elif choice == 'q':
            return
        else:
            return self.help_menu()

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
              created text NOT NULL
            );''')
        except sqlite3.OperationalError:
            print('DB already exists')

        # Committing changes and closing the connection to the database file
        conn.commit()
        conn.close()

    def add_todo(self):
        sqlite_file = 'todo_db.sqlite'  # name of the sqlite database file
        content = input('Enter new todo > ')
        time_stamp = str(datetime.now())
        print(time_stamp)
        print(type(time_stamp))
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        sql = f'INSERT INTO todos (content, created) VALUES ({content}, {time_stamp});'
        c.execute(sql)
        conn.commit()
        conn.close()
        return self.help_menu()

    def remove_todo(self):
        pass

    def list_all_todos(self):
        sqlite_file = 'todo_db.sqlite'  # name of the sqlite database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        sql = 'SELECT * FROM todos'
        c.execute(sql)
        all_rows = c.fetchall()
        print("All todos: ")
        for row in all_rows:
            print(f'{row[0]}: {row[1]}')

        conn.close()

        what_next = input("Show menu? [y/n]")
        if what_next == 'y' or what_next == 'yes':
            return self.help_menu()
        else:
            return

    def search_todos(self):
        pass


app = TODOApp()
app.start()
