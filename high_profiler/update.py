"""Update will go by symbol, only pulling necessary symbols to build graphs"""

import graph
import helper

symbols = helper.get_todays_symbols()  # Gets today's symbols
symbol_map = helper.get_symbol_map()  # Ties symbols to stock objects.

current_symbols = submap(symbol_map, symbols)  # Todays stock map
current_highs = [find_high(x) for x in current_symbols]

##Add horizons later. For now, also only do one type of submarket: sector

for sector in sectors:
    graphs[sector] = graphs.init()

for symbol in current_symbols:
    graphs[symbol.sector].add(symbol)