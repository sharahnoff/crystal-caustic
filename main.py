import csv
from tkinter import *
from tkinter import ttk
from crystal import *
import tkinter as tk
import calcualtions as calcs
import data
import speed_frame as sf
import group_speed_frame as gsf
import matplotlib.pyplot as plt
import surface_curve_frame as scf
import caustic_frame as cf
import iso3d_frame as iso3d


elements = {}
new = []
elementbox = None
c1_entry = None
c2_entry = None
c4_entry = None
p_entry = None
w_entry = None
root = None


def load_constants():
    crystals = data.load_crystals()
    for cr in crystals:
        if cr.saved:
            elements[cr.name + ' saved'] = cr
        else:
            elements[cr.name] = cr


def element_selected(event):
    c1_entry.delete(0, END)
    c4_entry.delete(0, END)
    p_entry.delete(0, END)
    c2_entry.delete(0, END)
    selection = elementbox.get()
    c1_entry.insert(0, elements[selection].c1)
    c2_entry.insert(0, elements[selection].c2)
    c4_entry.insert(0, elements[selection].c4)
    p_entry.insert(0, elements[selection].p)


def check_input():
    element = elementbox.get()
    if element:
        try:
            c1 = float(c1_entry.get())
            c4 = float(c4_entry.get())
            p = float(p_entry.get())
            c2 = float(c2_entry.get())
            return (element, c1, c2, c4, p)
        except ValueError:
            return False


def update_elementbox():
    elementbox.configure(values=list(elements.keys()))


def create_frames(notebook, cr):
    sf.create_speed_frame(notebook, cr)
    iso3d.create_frame(notebook, cr)
    gsf.create_group_speed_frame(notebook, cr)
    scf.create_surface_curve_frame(notebook, cr)
    cf.create_caustic_frame(notebook, cr)


def calculate(notebook):
    element = check_input()
    if not element:
        tk.messagebox.showwarning("Внимание", "Введены некорректные константы", icon="question")
    cr = None
    if element[0] in elements.keys():
        cr = Crystal(element[0], element[1], element[2], element[3], element[4])
        if not cr == elements[element[0]]:
            name = element[0] + '*'
            while name in elements.keys():
                name = element[0] + '*'
            cr.name = name
            new.append(name)
            elements[cr.name + ' calc-d'] = cr
        else:
            cr = elements[element[0]]
            if cr.saved or cr.calculated:
                if not tk.messagebox.askokcancel("Внимание", "Имеются вычисленые значения.\nПересчитать значения?", icon="question"):
                    return
            elements[cr.name + ' calc-d'] = elements.pop(element[0])
    else:
        cr = Crystal(element[0], element[1], element[2], element[3], element[4])
        elements[cr.name + ' calc-d'] = cr
    plt.close('all')
    cr.calculate()
    create_frames(notebook, cr)
    update_elementbox()
    elementbox.current(len(elements) - 1)


def on_closing():
    unsaved = []
    for name, cr in elements.items():
        if not cr.saved and cr.calculated:
            unsaved.append(cr.name)
    crls = ', '.join(unsaved)
    if len(unsaved) > 0:
        if tk.messagebox.askokcancel("Внимание", f"Есть несохраненные вичисления для: {crls}\nЗакрыть приложение?", icon="question"):
            plt.close('all')
            root.destroy()
    else:
        if tk.messagebox.askokcancel("Выход", f"Закрыть приложение?", icon="question"):
            plt.close('all')
            root.destroy()


def load_data(notebook):
    element = elementbox.get()
    if element:
        cr = elements[element]
        if not cr.calculated:
            check = data.load_data(cr)
            if not check:
                tk.messagebox.showwarning("Внимание", "Не найдено вычисленных значений для данного кристала", icon="question")
                return
        plt.close('all')
        create_frames(notebook, cr)
    else:
        tk.messagebox.showwarning("Внимание", "Выберите кристалл для загрузки значений", icon="question")


def save_data():
    element = elementbox.get()
    if element not in elements.keys():
        tk.messagebox.showwarning("Внимание", "Выберите кристалл для загрузки значений", icon="question")
        return
    cr = elements[element]
    if cr.name in new and not cr.saved:
        with open('elements.csv', 'a', encoding='utf-8', newline='\n') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow([element, c1_entry.get(), c2_entry.get(), c4_entry.get(), p_entry.get()])
    if data.save_data(cr):
        cr.saved = True
        tk.messagebox.showwarning("Внимание", "Данные успешно сохранены", icon="question")
    else:
        tk.messagebox.showwarning("Внимание", "Не получилось сохранить вычисления", icon="question")


def main():
    global root, elementbox, elements, c1_entry, c2_entry, c4_entry, p_entry, w_entry
    root = Tk()
    root.title("CAUSTICS")
    root.geometry("1280x980")
    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=BOTH)
    frame1 = ttk.Frame(notebook)
    frame1.pack(fill=BOTH, expand=True)
    for c in range(2): root.columnconfigure(index=c, weight=c)
    for r in range(8): root.rowconfigure(index=r, weight=1)
    ttk.Label(frame1, text='Выберите или введите константы').grid(row=0, column=0, columnspan=2, ipadx=4, ipady=4, padx=4, pady=4)
    ttk.Label(frame1, text='Название элемента').grid(row=1, column=0, ipadx=4, ipady=4, padx=4, pady=4)
    ttk.Label(frame1, text='Модуль С11 (10^12 дин/см^2)').grid(row=2, column=0, ipadx=4, ipady=4, padx=4, pady=4)
    c1_entry = ttk.Entry(frame1)
    c1_entry.grid(row=2, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    ttk.Label(frame1, text='Модуль С12 (10^12 дин/см^2)').grid(row=3, column=0, ipadx=4, ipady=4, padx=4, pady=4)
    c2_entry = ttk.Entry(frame1)
    c2_entry.grid(row=3, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    ttk.Label(frame1, text='Модуль С44 (10^12 дин/см^2)').grid(row=4, column=0, ipadx=4, ipady=4, padx=4, pady=4)
    c4_entry = ttk.Entry(frame1)
    c4_entry.grid(row=4, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    ttk.Label(frame1, text='Плотность р (г/см^3)').grid(row=5, column=0, ipadx=4, ipady=4, padx=4, pady=4)
    p_entry = ttk.Entry(frame1)
    p_entry.grid(row=5, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    #ttk.Label(frame1, text='w (рад/с)').grid(row=6, column=0, ipadx=4, ipady=4, padx=4, pady=4)
    #w_entry = ttk.Entry(frame1)
    #w_entry.grid(row=6, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    load_constants()
    elementbox = ttk.Combobox(frame1, values=list(elements.keys()))
    elementbox.grid(row=1, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    elementbox.bind("<<ComboboxSelected>>", element_selected)
    calc_button = ttk.Button(frame1, text='Рассчитать характеристики', command=lambda: calculate(notebook))
    calc_button.grid(row=6, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    save_button = ttk.Button(frame1, text='Сохранить характеристики', command=lambda: save_data())
    save_button.grid(row=7, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    save_button = ttk.Button(frame1, text='Загрузить характеристики', command=lambda: load_data(notebook))
    save_button.grid(row=8, column=1, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
    notebook.add(frame1, text="Выбор элемента")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


main()