import Tkinter as Tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plotcode():
    x = np.linspace(0, 2*np.pi)
    fig = Figure(figsize=(3, 3))
    ax = fig.add_subplot(111)
    ax.plot(x, x**2)

    return fig

root = Tk.Tk()
fig = plotcode()


def make_graph(fig, x, y):
    label = Tk.Label(text="Graph Name!")
    label.grid(row=x, column=y)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=x+1, column=y)


for x in range(0,6,2):
    for y in range(0,6,2):
        make_graph(fig, x, y)

root.mainloop()