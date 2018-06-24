import sqlite3
from datetime import datetime, date

# print(date.today())  # => 2018-06-22
# print(datetime.now())  # => 2018-06-22 12:42:23.854477


class TODOApp:
    def __init__(self):
        self.sqlite_file = 'todoapp.sqlite'
        self.conn = sqlite3.connect(self.sqlite_file)
        self.c = self.conn.cursor()

    def start(self):
        todo_item = TODOItems()
        return todo_item.help_menu()


class TODOLists(TODOApp):
    def __init__(self):
        super().__init__()


class TODOItems(TODOApp):
    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        # Creating a new SQLite table for countries
        try:
            self.c.execute('''
            CREATE TABLE todos (
              todo_id integer PRIMARY KEY,
              content text NOT NULL,
              created text NOT NULL
            );''')
        except sqlite3.OperationalError:
            print('DB already exists')

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

    def add_todo(self):
        content = input('Enter new todo > ')
        time_stamp = str(datetime.now())
        # sql = 'INSERT INTO todos (content, created) VALUES ({}, {});'.format(content, time_stamp)
        self.c.execute("""INSERT INTO todos (content, created) VALUES (?, ?)""", (content, time_stamp))
        print(f'{content} added at : {time_stamp}')
        return self.help_menu()

    def remove_todo(self):
        index = input('Enter index of todo to delete > ')
        self.c.execute("""DELETE FROM todos WHERE todo_id = ?""", index)
        return self.help_menu()

    def list_all_todos(self):
        self.c.execute('''SELECT * FROM todos''')
        all_rows = self.c.fetchall()
        print("All todos: ")
        for row in all_rows:
            print(f'{row[0]}: {row[1]}')

        what_next = input("Show menu? [y/n]")
        if what_next == 'y' or what_next == 'yes':
            return self.help_menu()
        else:
            return

    def search_todos(self):
        item = input('What are you looking for?  > ')
        if item.isdigit():
            try:
                self.c.execute("""SELECT * FROM todos WHERE todo_id=?""", item)
            except sqlite3.ProgrammingError:
                choice = input(f"Todo number {item} not found. \n\n's' to search again"
                               f"\n'h' for help menu\n'q' to quit\n> ")
                if choice == 's':
                    return self.search_todos()
                elif choice == 'q':
                    return
                else:
                    return self.help_menu()
        else:
            try:
                self.c.execute("""SELECT * FROM todos WHERE content LIKE '%?%'""")
            except sqlite3.ProgrammingError:
                choice = input(f"Todo containing {item} not found. \n\n's' to search again"
                               f"\n'h' for help menu\n'q' to quit\n> ")
                if choice == 's':
                    return self.search_todos()
                elif choice == 'q':
                    return
                else:
                    return self.help_menu()
        data = self.c.fetchone()
        print(data)
        return self.help_menu()


app = TODOApp()
app.start()
