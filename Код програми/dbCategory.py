import sqlite3
from dbWorkWith import *

class DbCategories(Db):
    # Створення таблиці Categories
    def create_category(self, name):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO Categories (name) VALUES (?)
            ''', (name,))
            connection.commit()

    # Видалення категорії за ідентифікатором
    def delete_category(self,category_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            DELETE FROM Categories WHERE id = ?
            ''', (category_id,))
            cursor.execute('SELECT COUNT(*) FROM Income WHERE category_id = ?', (category_id,))
            income_count = cursor.fetchone()[0]
            if income_count > 0:
                cursor.execute('''
                DELETE FROM Income WHERE category_id = ?
                ''', (category_id,))
                self.update_income_ids()

            cursor.execute('SELECT COUNT(*) FROM Expenses WHERE category_id = ?', (category_id,))
            expenses_count = cursor.fetchone()[0]
            if expenses_count > 0:
                cursor.execute('''
                DELETE FROM Expenses WHERE category_id = ?
                ''', (category_id,))
                self.update_expense_ids()

    # Зміна назви категорії за ідентифікатором
    def update_category(self,category_id, new_name):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
               UPDATE Categories SET name = ? WHERE id = ?
               ''', (new_name, category_id))
            connection.commit()

    # Функція для виведення всіх категорій
    def print_all_categories(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Categories')
            categories = cursor.fetchall()
        return categories

    # Функція для оновлення ID у таблиці Income
    def update_income_ids(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TEMPORARY TABLE Income_backup AS SELECT * FROM Income;
            ''')
            cursor.execute('''
            DELETE FROM Income;
            ''')
            cursor.execute('''
            INSERT INTO Income (account_id, category_id, count, date)
            SELECT account_id, category_id, count, date FROM Income_backup;
            ''')
            cursor.execute('''
            DROP TABLE Income_backup;
            ''')
            connection.commit()

    # Функція для оновлення ID у таблиці Expenses
    def update_expense_ids(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TEMPORARY TABLE Expenses_backup AS SELECT * FROM Expenses;
            ''')
            cursor.execute('''
            DELETE FROM Expenses;
            ''')
            cursor.execute('''
            INSERT INTO Expenses (account_id, category_id, count, date)
            SELECT account_id, category_id, count, date FROM Expenses_backup;
            ''')
            cursor.execute('''
            DROP TABLE Expenses_backup;
            ''')
            connection.commit()