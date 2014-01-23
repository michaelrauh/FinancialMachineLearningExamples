"""This module is concerned with generating stats from stock data"""

import math
import cPickle as pickle
from helper import *

stocks = pickle.load(open("pickles/stocks.p","rb"))

all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock))

for stock in all_points:
    normalize(stock)

# Produce map from years to buy/sell to list of data. Eg. years[2008][True][0][0] => Open of first good stock in 2008
years= {}
for stock in all_points:
    for date in stock:
        good = good_buy (date,stock[date])
        year = int(date[0:4])
        if not year in years:
            years[year] = {}
            years[year][True] = []
            years[year][False] = []
        years[year][good].append(stock[date])

pickle.dump(years,open("pickles/years.p","wb"))
