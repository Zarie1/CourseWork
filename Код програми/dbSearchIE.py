import sqlite3

class DbSearch:
    def get_connection(self):
        return sqlite3.connect('database.db')
    def create_db(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            ''')

            # Створення таблиці Account
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Account (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                balance INTEGER DEFAULT 0
            )
            ''')

            # Створення таблиці Income з account_id і date
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Income (
                id INTEGER PRIMARY KEY,
                account_id INTEGER,
                category_id INTEGER NOT NULL,
                count INTEGER,
                date TEXT,
                FOREIGN KEY (category_id) REFERENCES Categories(id),
                FOREIGN KEY (account_id) REFERENCES Account(id)
            )
            ''')

            # Створення таблиці Expenses з account_id і date
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY,
                account_id INTEGER,
                category_id INTEGER NOT NULL,
                count INTEGER,
                date TEXT,
                FOREIGN KEY (category_id) REFERENCES Categories(id),
                FOREIGN KEY (account_id) REFERENCES Account(id)
            )
            ''')

            # Створення тригерів для оновлення балансу в таблиці Account при вставці запису в таблицю Income
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_balance_after_income_insert
            AFTER INSERT ON Income
            FOR EACH ROW
            BEGIN
                UPDATE Account
                SET balance = balance + NEW.count
                WHERE id = NEW.account_id;
            END;
            ''')

            # Створення тригерів для оновлення балансу в таблиці Account при видаленні запису з таблиці Income
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_balance_after_income_delete
            AFTER DELETE ON Income
            FOR EACH ROW
            BEGIN
                UPDATE Account
                SET balance = balance - OLD.count
                WHERE id = OLD.account_id;
            END;
            ''')

            # Створення тригерів для оновлення балансу в таблиці Account при оновленні запису в таблиці Income
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_balance_after_income_update
            AFTER UPDATE OF account_id ON Income
            FOR EACH ROW
            BEGIN
                UPDATE Account
                SET balance = balance - OLD.count
                WHERE id = OLD.account_id;
        
                UPDATE Account
                SET balance = balance + NEW.count
                WHERE id = NEW.account_id;
            END;
            ''')

            # Створення тригерів для оновлення балансу в таблиці Account при вставці запису в таблицю Expenses
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_balance_after_expenses_insert
            AFTER INSERT ON Expenses
            FOR EACH ROW
            BEGIN
                UPDATE Account
                SET balance = balance - NEW.count
                WHERE id = NEW.account_id;
            END;
            ''')

            # Створення тригерів для оновлення балансу в таблиці Account при видаленні запису з таблиці Expenses
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_balance_after_expenses_delete
            AFTER DELETE ON Expenses
            FOR EACH ROW
            BEGIN
                UPDATE Account
                SET balance = balance + OLD.count
                WHERE id = OLD.account_id;
            END;
            ''')

            # Створення тригерів для оновлення балансу в таблиці Account при оновленні запису в таблиці Expenses
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_balance_after_expenses_update
            AFTER UPDATE OF account_id ON Expenses
            FOR EACH ROW
            BEGIN
                UPDATE Account
                SET balance = balance + OLD.count
                WHERE id = OLD.account_id;
        
                UPDATE Account
                SET balance = balance - NEW.count
                WHERE id = NEW.account_id;
            END;
            ''')
            connection.commit()
    #Пошук та вивід доходів за назвою категорії
    def search_income_by_category(self,category_name):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
                FROM Income
                INNER JOIN Categories ON Income.category_id = Categories.id
                INNER JOIN Account ON Income.account_id = Account.id
                WHERE Categories.name = ?
            ''', (category_name,))
            rows = cursor.fetchall()  # Якщо не має підходящої категорії, список пустий
        return rows

    #Пошук та вивід витрат за назвою категорії
    def search_expenses_by_category(self,category_name):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
                FROM Expenses
                INNER JOIN Categories ON Expenses.category_id = Categories.id
                INNER JOIN Account ON Expenses.account_id = Account.id
                WHERE Categories.name = ?
            ''', (category_name,))
            rows = cursor.fetchall()
        return rows

    #Пошук та вивід доходів за сумою
    def search_income_by_amount(self, amount):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
                FROM Income
                INNER JOIN Categories ON Income.category_id = Categories.id
                INNER JOIN Account ON Income.account_id = Account.id
                WHERE Income.count = ?
            ''', (amount,))
            rows = cursor.fetchall()
        return rows

    #Пошук та вивід доходів за датою
    def search_income_by_date(self, date):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
                FROM Income
                INNER JOIN Categories ON Income.category_id = Categories.id
                INNER JOIN Account ON Income.account_id = Account.id
                WHERE Income.date = ?
            ''', (date,))
            rows = cursor.fetchall()
        return rows

    #Пошук та вивід витрат за сумою
    def search_expenses_by_amount(self, amount):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
                FROM Expenses
                INNER JOIN Categories ON Expenses.category_id = Categories.id
                INNER JOIN Account ON Expenses.account_id = Account.id
                WHERE Expenses.count = ?
            ''', (amount,))
            rows = cursor.fetchall()
        return rows

    #Пошук та вивід витрат за датою
    def search_expenses_by_date(self, date):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
                FROM Expenses
                INNER JOIN Categories ON Expenses.category_id = Categories.id
                INNER JOIN Account ON Expenses.account_id = Account.id
                WHERE Expenses.date = ?
            ''', (date,))
            rows = cursor.fetchall()
        return rows