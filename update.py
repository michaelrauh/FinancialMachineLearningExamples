import graph
import stock
import cPickle as pickle

stocks = stock.get_todays_stocks()
today = stocks[0].today # TODO: Find a clean way to save this one time, and verify that it is correct

graphs = dict()
graphs["all"] = graph.Graph("all")

for current_stock in stocks:
    if current_stock.sector not in graphs:
        graphs[current_stock.sector] = graph.Graph(current_stock.sector)
    graphs[current_stock.sector].add(current_stock.symbol, current_stock.high_number)
    graphs["all"].add(current_stock.symbol, current_stock.high_number)

f = open("data/pickles/all_stocks.p", 'rb')
all_graphs = pickle.load(f)

all_graphs[today] = graphs

pickle.dump(all_graphs, f)