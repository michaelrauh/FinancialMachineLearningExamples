import Tkinter as Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot(graph):
    fig = Figure(figsize=(3, 3))
    ax = fig.add_subplot(111)
    ax.set_autoscaley_on(False)
    ax.set_ylim([0, 30])
    ax.set_xlim([0, 30])
    y = list()
    for bar in graph.bars.values():
        y.append(bar.size())

    # TODO: Make this smarter. Perhaps pick the largest graph's max
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