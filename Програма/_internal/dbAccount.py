import sqlite3
from dbWorkWith import *

class DbAccount(Db):
    # Створення таблиці Account
    def create_account(self, name, type):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO Account (name, type) VALUES (?, ?)
            ''', (name, type))
            connection.commit()

    # Видалення рахунку за ідентифікатором
    def delete_account(self, account_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            DELETE FROM Account WHERE id = ?
            ''', (account_id,))
            cursor.execute('''
            UPDATE Account SET id = id - 1 WHERE id > ?
            ''', (account_id,))
            connection.commit()

    # Зміна назви рахунку за ідентифікатором
    def update_account(self, account_id, new_name):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            UPDATE Account SET name = ? WHERE id = ?
            ''', (new_name, account_id))
            connection.commit()

    # Зміна типу рахунку за ідентифікатором
    def update_account_type(self, account_id, new_type):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            UPDATE Account SET type = ? WHERE id = ?
            ''', (new_type, account_id))
            connection.commit()

    # Функція для виведення даних з таблиці Account
    def print_account_data(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT * FROM Account
            ''')
            rows = cursor.fetchall()
        return rows