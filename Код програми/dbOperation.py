import sqlite3

def get_connection():
    return sqlite3.connect('database.db')

# Додавання до таблиці Income
def add_income(account_id, category_id, count, date):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO Income (account_id, category_id, count, date) VALUES (?, ?, ?, ?)
        ''', (account_id, category_id, count, date))
        connection.commit()

# Видалення з таблиці Income за ідентифікатором
def delete_income(income_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        DELETE FROM Income WHERE id = ?
        ''', (income_id,))
        cursor.execute('''
        UPDATE Income SET id = id - 1 WHERE id > ?
        ''', (income_id,))
        connection.commit()

# Зміна значення account_id у записі таблиці Income
def update_income_account_id(income_id, new_account_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        UPDATE Income SET account_id = ? WHERE id = ?
        ''', (new_account_id, income_id))
        connection.commit()

# Додавання до таблиці Expenses
def add_expense(account_id, category_id, count, date):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO Expenses (account_id, category_id, count, date) VALUES (?, ?, ?, ?)
        ''', (account_id, category_id, count, date))
        connection.commit()

# Видалення з таблиці Expenses за ідентифікатором
def delete_expense(expense_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        DELETE FROM Expenses WHERE id = ?
        ''', (expense_id,))
        cursor.execute('''
        UPDATE Expenses SET id = id - 1 WHERE id > ?
        ''', (expense_id,))
        connection.commit()

# Зміна значення account_id у записі таблиці Expenses
def update_expense_account_id(expense_id, new_account_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        UPDATE Expenses SET account_id = ? WHERE id = ?
        ''', (new_account_id, expense_id))
        connection.commit()

# Функція для виведення даних з таблиці Income
def print_income_data():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        SELECT Income.id, Account.name AS account_name, Categories.name AS category_name, Income.count, Income.date
        FROM Income
        INNER JOIN Categories ON Income.category_id = Categories.id
        INNER JOIN Account ON Income.account_id = Account.id
        ''')
        rows = cursor.fetchall()
        print("\nIncome data:")
        for row in rows:
            print(f"Income ID: {row[0]}, Account Name: {row[1]}, Category Name: {row[2]}, Count: {row[3]}, Date: {row[4]}")
    return rows

# Функція для виведення даних з таблиці Expenses
def print_expenses_data():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
        SELECT Expenses.id, Account.name AS account_name, Categories.name AS category_name, Expenses.count, Expenses.date
        FROM Expenses
        INNER JOIN Categories ON Expenses.category_id = Categories.id
        INNER JOIN Account ON Expenses.account_id = Account.id
        ''')
        rows = cursor.fetchall()
        print("\nExpenses data:")
        for row in rows:
            print(f"Expenses ID: {row[0]}, Account Name: {row[1]}, Category Name: {row[2]}, Count: {row[3]}, Date: {row[4]}")
    return rows