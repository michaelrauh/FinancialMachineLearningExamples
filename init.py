import stock
import graph
# import hasher

stocks = stock.get_all_stocks()

# TODO : Build graphs and save them
# TODO: Integrate update to save new graphs into same structure

# graphs = dict()
# graphs["all"] = graph.Graph("all")
#
# for symbol in symbols:
#             data = scraper.get_data(symbol, stock_data[symbol][0])
#             dates = stock.find_highs(data)
#             for date in dates:
#                 number = stock.get_high_number(date)
#                 graphs[date][stock_data[symbol][1]].add(symbol, number)

# hashes = dict()
# for graph in graphs:
#     hashes[hasher.hash(graph)] = graph
#
# pickle.dump(hashes)