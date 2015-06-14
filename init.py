# import parser
# import scraper
# import stock
# import graph
# import hasher
#
# # TODO: Move stock logic into stock class and call get_all_stocks
#
# stock_data = parser.parse_static_info()
# symbols = stock_data.keys()
#
# graphs = dict()
# graphs["all"] = graph.Graph("all")
#
# for symbol in symbols:
#     data = scraper.get_data(symbol, stock_data[symbol][0])
#     dates = stock.find_highs(data)
#     for date in dates:
#         number = stock.get_high_number(date)
#         graphs[date][stock_data[symbol][1]].add(symbol, number)
#
# hashes = dict()
# for graph in graphs:
#     hashes[hasher.hash(graph)] = graph
#
# pickle.dump(hashes)