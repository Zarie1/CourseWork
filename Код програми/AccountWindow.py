from tkinter import *
from tkinter.ttk import Treeview
from dbAccount import *

class Account(Toplevel):
    def __init__(self):
        super().__init__(master = None)
        self.title("Управління рахунками")
        self.geometry("260x400")
        self.resizable(False,False)

        Label(self, text="Назва рахунку", font="Arial 12").place(x=20, y=0)
        Label(self, text="Id", font="Arial 12").place(x=190, y=0)

        self.createCategoryText = Entry(self, width=20, font="Arial 10", bg="snow")
        self.createCategoryText.place(x=10, y=25)

        Button(self, text="Додати категорію", font="Arial 12", width=16, height=1).place(x=50, y=60)
        Button(self, text="Видалити категорію", font="Arial 12", width=16, height=1).place(x=50, y=100)
        Button(self, text="Змінити категорію", font="Arial 12", width=16, height=1).place(x=50, y=140)

        self.updateIdList()

        self.table = Treeview(self, columns=("ID", "Назва", "Тип", "Баланс"), show="headings", height=8,selectmode="browse")
        self.table.place(x=65, y=180)

        self.updateTable()

        headings = {"ID": 20, "Назва": 100}
        for head in headings:
            self.table.heading(head, text=head)
            self.table.column(head, anchor="center", width=headings[head])