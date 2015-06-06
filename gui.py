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
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=x, column=y)

for x in range(5):
    for y in range(5):
        make_graph(fig, x, y)


root.mainloop()