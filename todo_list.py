import sqlite3
from datetime import datetime
from todo_item import TODOItems


class TODOLists:
    def __init__(self, cursor, conn):
        self.conn = conn
        self.c = cursor
        self.create_table()

    def create_table(self):
        try:
            self.c.execute('''
            CREATE TABLE todoLists (
              list_id integer PRIMARY KEY,
              name text UNIQUE NOT NULL,
              created text NOT NULL
            );''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print('Table already exists')

    def help_menu(self):
        print('''
        Help Menu (TODO Lists):
        -------------------------
        'c' to create a new todo list
        'l' to list all lists
        'd' to delete a list
        'q' to quit
        ''')
        choice = input(' > ')
        if choice == 'c':
            return self.create_list()
        elif choice == 'l':
            self.list_all_lists()
        elif choice == 'd':
            return self.delete_list()
        elif choice == 'q':
            return
        else:
            return self.help_menu()

    def create_list(self):
        name = input('Name of new list > ')
        time_stamp = str(datetime.now())
        try:
            self.c.execute("""INSERT INTO todoLists (name, created) VALUES (?, ?)""", (name, time_stamp))
            self.conn.commit()
            print(f'List "{name}" created at : {time_stamp}')
            print("""
            'h' for help menu
            'f' to stat filling new todo list
            """)
            choice = input(" > ")
            if choice == 'f':
                sql = f"""SELECT list_id from todoLists WHERE name="{name}" """
                self.c.execute(sql)
                l_id = self.c.fetchone()
                print(l_id)
                return self.fill_list(l_id)
        except sqlite3.IntegrityError:
            return "List already exists"
        return self.help_menu()

    def fill_list(self, list_id):
        todo_items = TODOItems(list_id[0], self.c, self.conn)
        return todo_items.help_menu()

    def list_all_lists(self):
        self.c.execute('''SELECT * FROM todoLists''')
        all_rows = self.c.fetchall()
        print("All lists: ")
        for row in all_rows:
            print(f'{row[0]}: {row[1]}')

        what_next = input("Enter number of list to view or 'h' for help menu")
        if what_next == 'h':
            return self.help_menu()
        elif what_next.isdigit():
            try:
                todo_items = TODOItems(what_next, self.c, self.conn)
                return todo_items.help_menu()
            except sqlite3.IntegrityError:
                print(f"Can't find list with number {what_next}")
                return self.help_menu()

    def delete_list(self):
        pass