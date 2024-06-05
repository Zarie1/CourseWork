import sqlite3

class Db():
    def get_connection(self):
        return sqlite3.connect('database.db')