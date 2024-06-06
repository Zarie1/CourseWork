from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from dbSearchIE import *
from CategoryWindow import *
from AccountWindow import *
from OperationWindow import *

class MainWin():
        def __init__(self):
                DbSearch().create_db()
        # Функція для пошуку за фільтрами та виводу результатів
        def search(self):
                self.table.delete(*self.table.get_children())
                if self.paramFilter.get() == "Категорія" and self.typesFilter.get() == "Прибутки":
                        rows = DbSearch().search_income_by_category(self.Filter.get().lower())
                        for row in rows:self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                        self.Filter.delete(0,END)
                elif self.paramFilter.get() == "Категорія" and self.typesFilter.get() == "Витрати":
                        rows = DbSearch().search_expenses_by_category(self.Filter.get().lower())
                        for row in rows:self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                        self.Filter.delete(0, END)
                elif self.paramFilter.get() == "Сума" and self.typesFilter.get() == "Прибутки":
                        try:
                                rows = DbSearch().search_income_by_amount(int(self.Filter.get()))
                                for row in rows:self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                                self.Filter.delete(0, END)
                        except ValueError:
                                rows = DbSearch().search_income_by_amount(self.Filter.get())
                                for row in rows: self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                                self.Filter.delete(0, END)
                elif self.paramFilter.get() == "Сума" and self.typesFilter.get() == "Витрати":
                        try:
                                rows = DbSearch().search_expenses_by_amount(int(self.Filter.get()))
                                for row in rows:self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                                self.Filter.delete(0, END)
                        except ValueError:
                                messagebox.showerror("Введіть ціле число")
                                rows = DbSearch().search_expenses_by_amount(self.Filter.get())
                                for row in rows: self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                                self.Filter.delete(0, END)
                elif self.paramFilter.get() == "Дата" and self.typesFilter.get() == "Прибутки":
                        rows = DbSearch().search_income_by_date(self.Filter.get())
                        for row in rows:self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                        self.Filter.delete(0, END)
                elif self.paramFilter.get() == "Дата" and self.typesFilter.get() == "Витрати":
                        rows = DbSearch().search_expenses_by_date(self.Filter.get())
                        for row in rows: self.table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                        self.Filter.delete(0, END)
        def doWin(self):
                mainwin = Tk()
                mainwin.title("Гаманець")
                mainwin.geometry("520x300")
                mainwin.resizable(False,False)

                self.Filter = Entry(mainwin, width=30, font="Arial 10", bg="snow")
                self.Filter.place(x=10,y=30)
                Label(mainwin, text="Фільтри пошуку", font="Arial 12").place(x=260,y=0)

                categories = ["Категорія","Сума","Дата"]
                self.paramFilter = StringVar(mainwin)
                self.paramFilter.set(categories[0] if categories else "")
                self.filterMenu = OptionMenu(mainwin, self.paramFilter, *categories)
                self.filterMenu.config(width=7,height=1,font="Arial 10")
                self.filterMenu.place(x=220, y=24)

                types = ["Прибутки","Витрати"]
                self.typesFilter = StringVar(mainwin)
                self.typesFilter.set(types[0] if types else "")
                self.typesMenu = OptionMenu(mainwin, self.typesFilter, *types)
                self.typesMenu.config(width=7,height=1,font="Arial 10")
                self.typesMenu.place(x=312, y=24)

                Button(mainwin, text="Пошук", font="Arial 12", width=7, height=1, command=self.search).place(x=405, y=24)
                Button(mainwin, text="Категорії", font="Arial 12", width=11, height=1, command=Category).place(x=400, y=80)
                Button(mainwin, text="Рахунки", font="Arial 12", width=11, height=1, command=Account).place(x=400, y=120)
                Button(mainwin, text="Операції", font="Arial 12", width=11, height=1, command=Operation).place(x=400, y=160)


                self.table = Treeview(mainwin, columns=("ID", "Рахунок", "Категорія", "Сума", "Дата"), show="headings", height=8, selectmode="browse")
                self.table.place(x=10, y=70)

                headings = {"ID": 20, "Рахунок": 100, "Категорія": 100, "Сума": 80, "Дата": 80}
                for head in headings:
                        self.table.heading(head, text=head)
                        self.table.column(head, anchor="center", width=headings[head])

                mainwin.mainloop()