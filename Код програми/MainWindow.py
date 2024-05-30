from tkinter import *
from tkinter.ttk import Treeview
from dbSearchIE import *
from CategoryWindow import *

# Функція для пошуку за фільтрами та виводу результатів
def search():
        table.delete(*table.get_children())
        if paramFilter.get() == "Категорія" and typesFilter.get() == "Прибутки":
                rows = search_income_by_category(Filter.get().lower())
                for row in rows:table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
        elif paramFilter.get() == "Категорія" and typesFilter.get() == "Витрати":
                rows = search_expenses_by_category(Filter.get().lower())
                for row in rows:table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
        elif paramFilter.get() == "Сума" and typesFilter.get() == "Прибутки":
                try:
                        rows = search_income_by_amount(int(Filter.get()))
                        for row in rows:table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                except ValueError:
                        rows = search_income_by_amount(Filter.get())
                        for row in rows: table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
        elif paramFilter.get() == "Сума" and typesFilter.get() == "Витрати":
                try:
                        rows = search_expenses_by_amount(int(Filter.get()))
                        for row in rows:table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                except ValueError:
                        rows = search_expenses_by_amount(Filter.get())
                        for row in rows: table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
        elif paramFilter.get() == "Дата" and typesFilter.get() == "Прибутки":
                rows = search_income_by_date(Filter.get())
                for row in rows:table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
        elif paramFilter.get() == "Дата" and typesFilter.get() == "Витрати":
                rows = search_expenses_by_date(Filter.get())
                for row in rows: table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
create_db()
mainwin = Tk()
mainwin.title("Гаманець")
mainwin.geometry("520x300")
mainwin.resizable(False,False)

Filter = Entry(mainwin, width=30, font="Arial 10", bg="snow")
Filter.place(x=10,y=30)
Label(mainwin, text="Фільтри пошуку", font="Arial 12").place(x=260,y=0)

categories = ["Категорія","Сума","Дата"]
paramFilter = StringVar(mainwin)
paramFilter.set(categories[0] if categories else "")
filterMenu = OptionMenu(mainwin, paramFilter, *categories)
filterMenu.config(width=7,height=1,font="Arial 10")
filterMenu.place(x=220, y=24)

types = ["Прибутки","Витрати"]
typesFilter = StringVar(mainwin)
typesFilter.set(types[0] if types else "")
typesMenu = OptionMenu(mainwin, typesFilter, *types)
typesMenu.config(width=7,height=1,font="Arial 10")
typesMenu.place(x=312, y=24)

Button(mainwin, text="Пошук", font="Arial 12", width=7, height=1, command=search).place(x=405, y=24)
Button(mainwin, text="Категорії", font="Arial 12", width=11, height=1, command=Category).place(x=400, y=80)
Button(mainwin, text="Рахунки", font="Arial 12", width=11, height=1).place(x=400, y=120)
Button(mainwin, text="Операції", font="Arial 12", width=11, height=1).place(x=400, y=160)


table = Treeview(mainwin, columns=("ID", "Рахунок", "Категорія", "Сума", "Дата"), show="headings", height=8, selectmode="browse")
table.place(x=10, y=70)

headings = {"ID": 20, "Рахунок": 100, "Категорія": 100, "Сума": 60, "Дата": 80}
for head in headings:
        table.heading(head, text=head)
        table.column(head, anchor="center", width=headings[head])

mainwin.mainloop()