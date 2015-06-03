import graph
import helper

symbols = helper.get_todays_symbols()
symbol_map = helper.get_todays_stocks(symbols)

current_highs = [find_high(x) for x in current_symbols]

graphs = dict()
graphs["all"] = graph.init()
for sector in sectors:
    graphs[sector] = graphsinit()

for symbol in current_symbols:
    graphs[symbol.sector].add(symbol)