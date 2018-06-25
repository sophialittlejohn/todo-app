import sqlite3
from todo_list import TODOLists


class TODOApp:
    def __init__(self):
        self.sqlite_file = 'todoapp.sqlite'
        self.conn = sqlite3.connect(self.sqlite_file)
        self.c = self.conn.cursor()

    def start(self):
        todo_lists = TODOLists(self.c, self.conn)
        return todo_lists.help_menu()


if __name__ == '__main__':
    app = TODOApp()
    app.start()

