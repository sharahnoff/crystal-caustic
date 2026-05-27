from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np


def add_speed_plot(axes, c, title, val1, val2):
    radians = np.linspace(0, np.pi * 2, len(val1[3]))
    axes[c].plot(radians, val1[3], label="t1")
    axes[c].plot(radians, val2[3], label="t2")
    axes[c].legend(fontsize=10)
    axes[c].set_title(title)


def fill_speed_frame(frame, cr):
    fig, axes = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
    add_speed_plot(axes, 0, 'в плоскости грани куба\n(10^5 см/с)', cr.t1, cr.t2)
    add_speed_plot(axes, 1, 'в диагональной плоскости\n(10^5 см/с)', cr.t1d, cr.t2d)
    fig.suptitle('Фазовая скорость', fontsize=14)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def add_iso_surface(axes, c, title, t1, t2, w):
    radians = np.linspace(0, np.pi * 2, len(t1))
    axes[c].plot(radians, [w / x for x in t1], label="t1")
    axes[c].plot(radians, [w / x for x in t2], label="t2")
    axes[c].legend(fontsize=10)
    axes[c].set_title(title)


def fill_iso_frame(frame, cr):
    fig, axes = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
    add_iso_surface(axes, 0, 'Плоскость грани\n(10^(-5) 1/см)', cr.t1[3], cr.t2[3], 1)
    add_iso_surface(axes, 1, 'Диаг. плоскость\n(10^(-5) 1/см)', cr.t1d[3], cr.t2d[3], 1)
    fig.suptitle('Изоэнергетическая поверхность', fontsize=14)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


check = False
frame1 = None
frame2 = None


def create_speed_frame(nb, cr):
    global check, frame1, frame2
    plt.close('all')
    if not check:
        frame1 = ttk.Frame(nb)
        frame1.pack(fill=BOTH, expand=True)
        nb.add(frame1, text="Фазовая скорость")
        frame2 = ttk.Frame(nb)
        frame2.pack(fill=BOTH, expand=True)
        nb.add(frame2, text="Изоэн. поверхность")
        check = True
    for widget in frame1.winfo_children():
        widget.destroy()
    for widget in frame2.winfo_children():
        widget.destroy()
    fill_speed_frame(frame1, cr)
    fill_iso_frame(frame2, cr)
