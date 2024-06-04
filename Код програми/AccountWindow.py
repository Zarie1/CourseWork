from tkinter import *
from tkinter.ttk import Treeview
from dbAccount import *

class Account(Toplevel):
    def __init__(self):
        super().__init__(master = None)
        self.title("Управління рахунками")
        self.geometry("400x470")
        self.resizable(False,False)

        Label(self, text="Введіть назву рахунку", font="Arial 12").place(x=85, y=0)
        Label(self, text="Введіть тип рахунку", font="Arial 12").place(x=90, y=50)
        Label(self, text="Id", font="Arial 12").place(x=300, y=20)

        self.accountTextName = Entry(self, width=20, font="Arial 10", bg="snow")
        self.accountTextName.place(x=90, y=25)

        self.accountTextType = Entry(self, width=20, font="Arial 10", bg="snow")
        self.accountTextType.place(x=90, y=75)


        Button(self, text="Додати рахунок", font="Arial 12", width=17, height=1, command=self.createAccount).place(x=130, y=110)
        Button(self, text="Видалити рахунок", font="Arial 12", width=17, height=1, command=self.deleteAccount).place(x=130, y=150)
        Button(self, text="Змінити назву рахунку", font="Arial 12", width=17, height=1, command=self.updateAccount).place(x=130, y=190)
        Button(self, text="Змінити тип рахунку", font="Arial 12", width=17, height=1, command=self.updateAccountData).place(x=130, y=230)

        self.updateIdList()

        self.table = Treeview(self, columns=("ID", "Назва", "Тип", "Баланс"), show="headings", height=8,selectmode="browse")
        self.table.place(x=50, y=270)

        self.updateTable()

        headings = {"ID": 20, "Назва": 100, "Тип": 100, "Баланс": 80}
        for head in headings:
            self.table.heading(head, text=head)
            self.table.column(head, anchor="center", width=headings[head])
    def getIdList(self):
        accounts = print_account_data()
        newList = []
        if accounts == []: newList.append("Пусто")
        else:
            for account in accounts:newList.append(account[0])
        return newList
    def updateIdList(self):
        accountes = self.getIdList()
        self.listId = StringVar(self)
        self.listId.set(accountes[0] if accountes else "")
        self.idMenu = OptionMenu(self, self.listId, *accountes)
        self.idMenu.config(width=7, height=1, font="Arial 10")
        self.idMenu.place(x=260, y=39)
    def updateTable(self):
        self.table.delete(*self.table.get_children())
        rows = print_account_data()
        for row in rows: self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3]))
    def createAccount(self):
        name = self.accountTextName.get().lower()
        type = self.accountTextType.get().lower()
        if name != "":
            create_account(name, type)
            self.updateIdList()
            self.updateTable()
            self.accountTextName.delete(0, END)
            self.accountTextType.delete(0, END)
    def deleteAccount(self):
        try:
            delete_account(int(self.listId.get()))
            self.updateIdList()
            self.updateTable()
        except ValueError: print("Пусто")
    def updateAccount(self):
        name = self.accountTextName.get().lower()
        if name != "":
            try:
                update_account(int(self.listId.get()),name)
                self.updateTable()
                self.accountTextName.delete(0, END)
            except ValueError:print("Пусто")
    def updateAccountData(self):
        type = self.accountTextType.get().lower()
        if type != "":
            try:
                update_account_type(int(self.listId.get()),type)
                self.updateTable()
                self.accountTextType.delete(0, END)
            except ValueError:print("Пусто")