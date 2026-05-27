from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
import data

check = False
Kframe = None
Aframe = None


def add_plot(axes, title, lbl,  values, r, c):
    radians = np.linspace(0, np.pi /2, len(values))
    axes[r,c].plot(radians, values, label=lbl)
    axes[r,c].set_xlabel('Theta, рад.')
    axes[r,c].legend(fontsize=10)
    axes[r,c].set_title(title)
    axes[r,c].grid(True)

def fill_frame(frame, title, lbl, values):
    fig, axes = plt.subplots(2,2)
    add_plot(axes,'В плоскости грани, мода t1', lbl, values[0], 0,0)
    add_plot(axes, 'В плоскости грани, мода t2', lbl, values[1], 0, 1)
    add_plot(axes, 'В диаг. плоскости, мода t1',lbl, values[2], 1, 0)
    add_plot(axes, 'В диаг. плоскости, мода t2',lbl, values[3], 1, 1)
    fig.suptitle(title, fontsize=14)
    plt.subplots_adjust(hspace=0.25)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

def create_surface_curve_frame(nb, cr):
    global check, Kframe, Aframe
    if not check:
        Kframe = ttk.Frame(nb)
        Kframe.pack(fill=BOTH, expand=True)
        nb.add(Kframe, text="Кривизна поверхности")
        Aframe = ttk.Frame(nb)
        Aframe.pack(fill=BOTH, expand=True)
        nb.add(Aframe, text="Коэффициент усиления")
        check = True
    for widget in Kframe.winfo_children():
        widget.destroy()
    for widget in Aframe.winfo_children():
        widget.destroy()
    fill_frame(Kframe, "Кривизна поверхности", 'K', (cr.t1[4], cr.t2[4], cr.t1d[4], cr.t2d[4]))
    fill_frame(Aframe, "Коэффициент усиления", 'A', (cr.t1[5], cr.t2[5], cr.t1d[5], cr.t2d[5]))