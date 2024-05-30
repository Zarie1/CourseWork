import sqlite3

def create_db():
    connection = sqlite3.connect('database.db')
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
    connection.close()
#Пошук та вивід доходів за назвою категорії
def search_income_by_category(category_name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
        FROM Income
        INNER JOIN Categories ON Income.category_id = Categories.id
        INNER JOIN Account ON Income.account_id = Account.id
        WHERE Categories.name = ?
    ''', (category_name,))
    rows = cursor.fetchall()  # Якщо не має підходящої категорії, список пустий
    connection.close()
    return rows

#Пошук та вивід витрат за назвою категорії
def search_expenses_by_category(category_name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
        FROM Expenses
        INNER JOIN Categories ON Expenses.category_id = Categories.id
        INNER JOIN Account ON Expenses.account_id = Account.id
        WHERE Categories.name = ?
    ''', (category_name,))
    rows = cursor.fetchall()
    connection.close()
    return rows

#Пошук та вивід доходів за сумою
def search_income_by_amount(amount):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
        FROM Income
        INNER JOIN Categories ON Income.category_id = Categories.id
        INNER JOIN Account ON Income.account_id = Account.id
        WHERE Income.count = ?
    ''', (amount,))
    rows = cursor.fetchall()
    connection.close()
    return rows

#Пошук та вивід доходів за датою
def search_income_by_date(date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
        FROM Income
        INNER JOIN Categories ON Income.category_id = Categories.id
        INNER JOIN Account ON Income.account_id = Account.id
        WHERE Income.date = ?
    ''', (date,))
    rows = cursor.fetchall()
    connection.close()
    return rows

#Пошук та вивід витрат за сумою
def search_expenses_by_amount(amount):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
        FROM Expenses
        INNER JOIN Categories ON Expenses.category_id = Categories.id
        INNER JOIN Account ON Expenses.account_id = Account.id
        WHERE Expenses.count = ?
    ''', (amount,))
    rows = cursor.fetchall()
    connection.close()
    return rows

#Пошук та вивід витрат за датою
def search_expenses_by_date(date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
        FROM Expenses
        INNER JOIN Categories ON Expenses.category_id = Categories.id
        INNER JOIN Account ON Expenses.account_id = Account.id
        WHERE Expenses.date = ?
    ''', (date,))
    rows = cursor.fetchall()
    connection.close()
    return rows

# Створення таблиці Account
def create_account(name, type):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO Account (name, type) VALUES (?, ?)
    ''', (name, type))
    connection.commit()
    connection.close()

# Видалення рахунку за ідентифікатором
def delete_account(account_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM Account WHERE id = ?
    ''', (account_id,))
    connection.commit()
    connection.close()

# Зміна назви рахунку за ідентифікатором
def update_account(account_id, new_name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE Account SET name = ? WHERE id = ?
    ''', (new_name, account_id))
    connection.commit()
    connection.close()

# Додавання до таблиці Income
def add_income(account_id, category_id, count, date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO Income (account_id, category_id, count, date) VALUES (?, ?, ?, ?)
    ''', (account_id, category_id, count, date))
    connection.commit()
    connection.close()

# Видалення з таблиці Income за ідентифікатором
def delete_income(income_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM Income WHERE id = ?
    ''', (income_id,))
    connection.commit()
    connection.close()

# Зміна значення account_id у записі таблиці Income
def update_income_account_id(income_id, new_account_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE Income SET account_id = ? WHERE id = ?
    ''', (new_account_id, income_id))
    connection.commit()
    connection.close()

# Додавання до таблиці Expenses
def add_expense(account_id, category_id, count, date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO Expenses (account_id, category_id, count, date) VALUES (?, ?, ?, ?)
    ''', (account_id, category_id, count, date))
    connection.commit()
    connection.close()

# Видалення з таблиці Expenses за ідентифікатором
def delete_expense(expense_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM Expenses WHERE id = ?
    ''', (expense_id,))
    connection.commit()
    connection.close()

# Зміна значення account_id у записі таблиці Expenses
def update_expense_account_id(expense_id, new_account_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE Expenses SET account_id = ? WHERE id = ?
    ''', (new_account_id, expense_id))
    connection.commit()
    connection.close()