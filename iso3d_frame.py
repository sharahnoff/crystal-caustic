from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
from matplotlib import cm

check = False
frame = None


def add_plot(fig, axes, title, values):
    X, Y, Z, R = values[0], values[1], values[2], values[3]
    surface = axes.plot_surface(X, Y, Z, rstride=2, cstride=1, facecolors=cm.jet((R - R.min()) / (R.max() - R.min())), linewidth=0, shade=False)
    axes.set_title(title)
    axes.set_xlabel('x, (10^(-5) 1/см)')
    axes.set_ylabel('y, (10^(-5) 1/см)')
    axes.set_zlabel('z, (10^(-5) 1/см)')
    #fig.colorbar(surface, shrink=0.1, aspect=5, ax=axes)
    return


def fill_frame(frame, cr):
    fig = plt.figure()
    ax1 = fig.add_subplot(1,2,1, projection='3d')
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    #fig, axes = plt.subplots(1, 2, projection='3d')
    add_plot(fig, ax1, 'для моды t1', cr.t13d)
    add_plot(fig, ax2, 'для моды t2', cr.t23d)
    fig.suptitle("Изоэнергетическая поверхность")
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def create_frame(nb, cr):
    global check, frame
    if not check:
        frame = ttk.Frame(nb)
        frame.pack(fill=BOTH, expand=True)
        nb.add(frame, text="Изоэн. поверхность 3D")
        check = True
    for widget in frame.winfo_children():
        widget.destroy()
    fill_frame(frame, cr)
