import Tkinter as Tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot(graph):
    fig = Figure(figsize=(3, 3))
    ax = fig.add_subplot(111)

    y = list()
    for bar in graph.bars.values():
        y.append(bar.size())

    x = range(len(y))
    ax.bar(x, y)

    return fig


def make_graph(root, graph, x, y):
    fig = plot(graph)
    label = Tk.Label(text=graph.sector)
    label.grid(row=x, column=y)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=x+1, column=y)


def show(graphs):
    root = Tk.Tk()
    x = 0
    for graph in graphs.values():
        make_graph(root, graph, x % 4, x/4)
        x += 2
    root.mainloop()