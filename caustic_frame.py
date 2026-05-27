from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import data

check = False
cframe = None
uframe = None

def get_values(vx, vz):
    vx = vx + [a * (-1) for a in vx]
    vz = vz + vz
    vx = vx + [a * (-1) for a in vx]
    vz = vz + [a * (-1) for a in vz]
    return vx, vz


def add_plot(axes, title, values):
    x, y = get_values(values[0], values[1])
    axes.scatter(x, y)
    axes.set_title(title)
    axes.set_xlabel('x/d')
    axes.set_ylabel('y/d')
    axes.set_xlim(-10, 10)
    axes.set_ylim(-10, 10)
    axes.grid(True)


def fill_frame(frame, cr, uni=False):
    fig = None
    if uni:
        fig, axes = plt.subplots(1, 1)
        add_plot(axes, 'Картина каустики', cr.t1c)
        add_plot(axes, 'Картина каустики', cr.t2c)
    else:
        fig, axes = plt.subplots(1, 2)
        add_plot(axes[0], 'Модa t1', cr.t1c)
        add_plot(axes[1], 'Модa t2', cr.t2c)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    mplcursors.cursor()
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def create_caustic_frame(nb, cr):
    global check, cframe, uframe
    if not check:
        cframe = ttk.Frame(nb)
        cframe.pack(fill=BOTH, expand=True)
        nb.add(cframe, text="Картины каустики")
        uframe = ttk.Frame(nb)
        uframe.pack(fill=BOTH, expand=True)
        nb.add(uframe, text="Картина каустики")
        check = True
    for widget in cframe.winfo_children():
        widget.destroy()
    for widget in uframe.winfo_children():
        widget.destroy()
    fill_frame(cframe, cr)
    fill_frame(uframe, cr, True)
