import stock
import graph
import cPickle as pickle
# import hasher

stocks = stock.get_all_stocks()
graphs = dict()

for current_stock in stocks:
    for date in current_stock.highs:
        if date not in graphs:
            graphs[date] = dict()
            graphs[date]["all"] = graph.Graph("all")
        if current_stock.sector not in graphs[date]:
            graphs[date][current_stock.sector] = graph.Graph(current_stock.sector)
        current_high_number = current_stock.all_high_numbers.pop()
        graphs[date][current_stock.sector].add(current_stock.symbol, current_high_number)
        graphs[date]["all"].add(current_stock.symbol, current_high_number)

f = open("data/pickles/all_stocks.p", 'wb')
pickle.dump(graphs, f)