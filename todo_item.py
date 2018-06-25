import sqlite3
from datetime import datetime


class TODOItems:
    def __init__(self, list_id, cursor, conn):
        self.c = cursor
        self.conn = conn
        self.create_table()
        self.list_id = list_id

    def create_table(self):
        try:
            self.c.execute('''
            CREATE TABLE todos (
              todo_id integer PRIMARY KEY,
              list_id integer NOT NULL,
              content text NOT NULL,
              created text NOT NULL,
              FOREIGN KEY(list_id) REFERENCES todoLists(list_id)
            );''')
        except sqlite3.OperationalError:
            print('Table already exists')

    def help_menu(self):
        print('''
        Help Menu (Items):
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
        self.c.execute("""INSERT INTO todos (content, created, list_id) VALUES (?, ?, ?)""",
                       (content, time_stamp, self.list_id))
        print(f'{content} added at {time_stamp}.')
        self.conn.commit()
        return self.help_menu()

    def remove_todo(self):
        index = input('Enter index of todo to delete > ')
        self.c.execute(f"""DELETE FROM todos WHERE todo_id = '{index}'""")
        self.conn.commit()
        return self.help_menu()

    def list_all_todos(self):
        self.c.execute(f'''SELECT * FROM todos WHERE list_id={self.list_id}''')
        all_rows = self.c.fetchall()
        print("All todos: ")
        for row in all_rows:
            print(f'{row[0]}: {row[2]}')

        what_next = input("Show menu? [y/n]")
        if what_next == 'y' or what_next == 'yes':
            return self.help_menu()
        else:
            return

    def search_todos(self):
        item = input('What are you looking for?  > ')
        if item.isdigit():
            try:
                self.c.execute(f"""SELECT * FROM todos WHERE todo_id=''{item}''""")
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
