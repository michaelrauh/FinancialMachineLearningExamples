import graph
import stock
import gui

stocks = stock.get_todays_stocks()

graphs = dict()
graphs["all"] = graph.Graph("all")

for current_stock in stocks:
    if current_stock.sector not in graphs:
        graphs[current_stock.sector] = graph.Graph(current_stock.sector)
    graphs[current_stock.sector].add(current_stock.symbol, current_stock.high_number)
    graphs["all"].add(current_stock.symbol, current_stock.high_number)

gui.show(graphs)