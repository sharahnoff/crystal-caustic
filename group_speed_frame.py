from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import mplcursors
import matplotlib.pyplot as plt
import numpy as np


def add_components_plot(axes, title, values, r, c):
    radians = np.linspace(0, np.pi / 2, int(len(values[0]) / 4))
    axes[r, c].plot(radians, values[0][:int(len(values[0]) / 4)], label="x")
    axes[r, c].plot(radians, values[1][:int(len(values[0]) / 4)], label="y", linestyle='--')
    axes[r, c].plot(radians, values[2][:int(len(values[0]) / 4)], label="z")
    axes[r, c].set_xlabel('Theta, рад.')
    axes[r, c].set_ylabel('V, 10^5 см/с')
    axes[r, c].legend(fontsize=10)
    axes[r, c].set_title(title)
    axes[r, c].grid(True)


def add_param_group_speed(axes, title, t1, t2, r, c):
    axes[r, c].plot(t1[0], t1[2], label='t1')
    axes[r, c].plot(t2[0], t2[2], label='t2', linestyle='--')
    axes[r, c].set_xlabel('Vx, 10^5 см/с')
    axes[r, c].set_ylabel('Vz, 10^5 см/с')
    axes[r, c].legend(fontsize=10)
    axes[r, c].set_title(title)
    axes[r, c].grid(True)


def add_param2_group_speed(axes, title, t1, t2, r, c):
    axes[r, c].plot([x / np.sqrt(2) for x in np.add(t1[0], t1[1])], t1[2], label='t1')
    axes[r, c].plot([x / np.sqrt(2) for x in np.add(t2[0], t2[1])], t2[2], label='t2', linestyle='--')
    axes[r, c].set_xlabel('(Vx+Vy)/sqrt(2), 10^5 см/с')
    axes[r, c].set_ylabel('Vz, 10^5 см/с')
    axes[r, c].legend(fontsize=10)
    axes[r, c].set_title(title)
    axes[r, c].grid(True)


def fill_frame(frame, t1, t2, second=False):
    fig, axes = plt.subplots(2, 2)
    add_components_plot(axes, 'Комп-ты груп. скорости моды t1', t1, 0, 0)
    add_components_plot(axes, 'Комп-ты груп. скорости моды t2', t2, 0, 1)
    add_param_group_speed(axes, 'Сечение волновой поверхности', t1, t2, 1, 0)
    if second:
        add_param2_group_speed(axes, '((Vx + Vy)/sqrt(2) ,Vz)', t1[:3], t2[:3], 1, 1)
        fig.suptitle('Групповая скорость в диаг. плоскости куба', fontsize=14)
    else:
        fig.suptitle('Групповая скорость в плоскости грани куба', fontsize=14)
    plt.subplots_adjust(hspace=0.25)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    mplcursors.cursor()
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


check = False
frame1 = None
frame2 = None


def create_group_speed_frame(nb, cr):
    global check, frame1, frame2
    if not check:
        frame1 = ttk.Frame(nb)
        frame1.pack(fill=BOTH, expand=True)
        frame2 = ttk.Frame(nb)
        frame2.pack(fill=BOTH, expand=True)
        nb.add(frame1, text="Групповая скорость п/г")
        nb.add(frame2, text="Групповая скорость д/п")
        check = True
    for widget in frame1.winfo_children():
        widget.destroy()
    for widget in frame2.winfo_children():
        widget.destroy()
    fill_frame(frame1, cr.t1[:3], cr.t2[:3])
    fill_frame(frame2, cr.t1d[:3], cr.t2d[:3], True)
