from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from dbCategory import *


class Category(Toplevel):
    def __init__(self):
        super().__init__(master = None)
        self.title("Управління категоріями")
        self.geometry("260x400")
        self.resizable(False,False)

        Label(self, text="Назва категорії", font="Arial 12").place(x=20, y=0)
        Label(self, text="Id", font="Arial 12").place(x=190, y=0)

        self.сategoryText = Entry(self, width=20, font="Arial 10", bg="snow")
        self.сategoryText.place(x=10, y=25)

        Button(self, text="Додати категорію", font="Arial 12", width=16, height=1, command=self.createCategory).place(x=50, y=60)
        Button(self, text="Видалити категорію", font="Arial 12", width=16, height=1, command=self.deleteCategory).place(x=50, y=100)
        Button(self, text="Змінити категорію", font="Arial 12", width=16, height=1, command=self.updateCategory).place(x=50, y=140)

        self.updateIdList()

        self.table = Treeview(self, columns=("ID", "Назва"), show="headings", height=8,selectmode="browse")
        self.table.place(x=65, y=180)

        headings = {"ID": 20, "Назва": 100}
        for head in headings:
            self.table.heading(head, text=head)
            self.table.column(head, anchor="center", width=headings[head])

        self.updateTable()

    def getIdList(self):
        categories = DbCategories().print_all_categories()
        newList = []
        if categories == []: newList.append("Пусто")
        else:
            for category in categories:newList.append(category[0])
        return newList
    def updateIdList(self):
        categories = self.getIdList()
        self.listId = StringVar(self)
        self.listId.set(categories[0] if categories else "Пусто")
        self.idMenu = OptionMenu(self, self.listId, *categories)
        self.idMenu.config(width=7, height=1, font="Arial 10")
        self.idMenu.place(x=152, y=19)
    def updateTable(self):
        self.table.delete(*self.table.get_children())
        rows = DbCategories().print_all_categories()
        for row in rows: self.table.insert('', 'end', values=(row[0], row[1]))
    def createCategory(self):
        name = self.сategoryText.get().lower()
        if name != "":
            DbCategories().create_category(name)
            self.updateIdList()
            self.updateTable()
            self.сategoryText.delete(0, END)
        else:
            messagebox.showerror("Помилка", "Заповніть поле з назвою категорії")
    def deleteCategory(self):
        try:
            DbCategories().delete_category(int(self.listId.get()))
            self.updateIdList()
            self.updateTable()
        except ValueError: messagebox.showerror("Помилка","Немає категорій для видалення")
    def updateCategory(self):
        name = self.сategoryText.get().lower()
        if name != "":
            try:
                DbCategories().update_category(int(self.listId.get()), name)
                self.updateTable()
                self.сategoryText.delete(0, END)
            except ValueError:messagebox.showerror("Помилка","Немає категорій для зміни")
        else:
            messagebox.showerror("Помилка", "Заповніть поле з новою назвою категорії")