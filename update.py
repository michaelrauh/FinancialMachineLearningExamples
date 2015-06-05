import graph
import stock

stocks = stock.get_todays_stocks()

for stock in stocks:
    print stock
# graphs = dict()
# graphs["all"] = graph.init()
# for sector in sectors:
#     graphs[sector] = graphsinit()
#
# for symbol in current_symbols:
#     graphs[symbol.sector].add(symbol)