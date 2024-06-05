from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from dbOperation import *
from dbCategory import DbCategories
from dbAccount import DbAccount

class Operation(Toplevel):
    def __init__(self):
        super().__init__(master = None)
        self.title("Управління витратами та доходами")
        self.geometry("430x650")
        self.resizable(False,False)

        Label(self, text="Введіть суму та дату:", font="Arial 12").place(x=20, y=5)
        Label(self, text="Введіть id операції:", font="Arial 12").place(x=20, y=40)
        Label(self, text="Тип операції", font="Arial 12").place(x=30, y=80)
        Label(self, text="Назва категорії", font="Arial 12").place(x=20, y=120)
        Label(self, text="Назва рахунку", font="Arial 12").place(x=20, y=160)
        Label(self, text="Таблиця доходів", font="Arial 12").place(x=160, y=215)
        Label(self, text="Таблиця витрат", font="Arial 12").place(x=160, y=435)

        self.operationText = Entry(self, width=20, font="Arial 10", bg="snow")
        self.operationText.place(x=180, y=9)

        self.operationId = Entry(self, width=10, font="Arial 10", bg="snow")
        self.operationId.place(x=170, y=44)

        Button(self, text="Додати", font="Arial 12", width=13, height=1, command=self.createOperation).place(x=290, y=80)
        Button(self, text="Видалити", font="Arial 12", width=13, height=1, command=self.deleteOperation).place(x=290, y=120)
        Button(self, text="Змінити рахунок", font="Arial 12", width=13, height=1, command=self.changeAccount).place(x=290, y=160)

        self.updateIdCategoriesList()

        self.updateIdAccountsList()

        types = ["Доходи", "Витрати"]
        self.typesFilter = StringVar(self)
        self.typesFilter.set(types[0] if types else "")
        self.typesMenu = OptionMenu(self, self.typesFilter, *types)
        self.typesMenu.config(width=7, height=1, font="Arial 10")
        self.typesMenu.place(x=165, y=78)

        self.tableIncome = Treeview(self, columns=("ID", "Рахунок", "Категорія", "Сума", "Дата"), show="headings", height=8, selectmode="browse")
        self.tableIncome.place(x=20, y=240)

        headings = {"ID": 20, "Рахунок": 100, "Категорія": 100, "Сума": 80, "Дата": 80}
        for head in headings:
            self.tableIncome.heading(head, text=head)
            self.tableIncome.column(head, anchor="center", width=headings[head])

        self.updateTableIncome()

        self.tableExpense = Treeview(self, columns=("ID", "Рахунок", "Категорія", "Сума", "Дата"), show="headings",height=8, selectmode="browse")
        self.tableExpense.place(x=20, y=460)

        for head in headings:
            self.tableExpense.heading(head, text=head)
            self.tableExpense.column(head, anchor="center", width=headings[head])

        self.updateTableExpense()
    def updateTableIncome(self):
        self.tableIncome.delete(*self.tableIncome.get_children())
        rows = DbOperatons().print_income_data()
        for row in rows: self.tableIncome.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
    def updateTableExpense(self):
        self.tableExpense.delete(*self.tableExpense.get_children())
        rows = DbOperatons().print_expenses_data()
        for row in rows: self.tableExpense.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
    def getNameAndDate(self):
        info = self.operationText.get().split(";")
        try:
            count = int(info[0])
            data = [int(i) for i in info[1].split("-")]
            return [count, info[1]]
        except ValueError:
            return ""
    def updateIdCategoriesList(self):
        self.allCategoryData = DbCategories().print_all_categories()
        categories = []
        if self.allCategoryData == []: categories.append("Пусто")
        else:
            for data in self.allCategoryData:categories.append(data[1])
        self.categoryName = StringVar(self)
        self.categoryName.set(categories[0] if categories else "")
        self.idCategoriesMenu = OptionMenu(self, self.categoryName, *categories)
        self.idCategoriesMenu.config(width=12, height=1, font="Arial 10")
        self.idCategoriesMenu.place(x=150, y=118)
    def updateIdAccountsList(self):
        self.allAccountsData = DbAccount().print_account_data()
        accountes = []
        self.listOfAccountData = []
        if self.allAccountsData == []: accountes.append("Пусто")
        else:
            for account in self.allAccountsData: accountes.append(account[1])
        self.accountName = StringVar(self)
        self.accountName.set(accountes[0] if accountes else "")
        self.idAccountMenu = OptionMenu(self, self.accountName, *accountes)
        self.idAccountMenu.config(width=12, height=1, font="Arial 10")
        self.idAccountMenu.place(x=150, y=158)
    def findAccountId(self):
        accountName = self.accountName.get()
        for account in self.allAccountsData:
            if account[1] == accountName:accountId = account[0]
        return int(accountId)
    def findCategoryId(self):
        categoryName = self.categoryName.get()
        for category in self.allCategoryData:
            if category[1] == categoryName:categoryId = category[0]
        return int(categoryId)
    def createOperation(self):
        nameAndDate = self.getNameAndDate()
        if nameAndDate != "":
            if self.accountName.get() != "Пусто" and self.categoryName.get() != "Пусто":
                if self.typesFilter.get() == "Доходи":
                    DbOperatons().add_income(self.findAccountId(), self.findCategoryId(), nameAndDate[0], nameAndDate[1])
                    self.updateTableIncome()
                else:
                    DbOperatons().add_expense(self.findAccountId(), self.findCategoryId(), nameAndDate[0], nameAndDate[1])
                    self.updateTableExpense()
            else:
                messagebox.showerror("Помилка", "Немає рахунків або категорій")
        else: messagebox.showerror("Помилка", "Неправильно заповнене поле! Приклад: 2000;2024-05-01")
    def deleteOperation(self):
        try:
            operationId = int(self.operationId.get())
            if self.typesFilter.get() == "Доходи":
                DbOperatons().delete_income(operationId)
                self.updateTableIncome()
                self.operationId.delete(0,END)
            else:
                DbOperatons().delete_expense(operationId)
                self.updateTableExpense()
                self.operationId.delete(0, END)
        except ValueError:
            messagebox.showerror("Помилка", "Немає відповідних операцій для видалення")
    def changeAccount(self):
        try:
            operationId = int(self.operationId.get())
            if self.accountName.get() != "Пусто":
                if self.typesFilter.get() == "Доходи":
                    DbOperatons().update_income_account_id(operationId, self.findAccountId())
                    self.updateTableIncome()
                    self.operationId.delete(0,END)
                else:
                    DbOperatons().update_expense_account_id(operationId, self.findAccountId())
                    self.updateTableExpense()
                    self.operationId.delete(0, END)
            else:messagebox.showerror("Помилка", "Немає відповідного рахунку для зміни")
        except ValueError:
            messagebox.showerror("Помилка", "Немає відповідних операцій для змін рахунку")