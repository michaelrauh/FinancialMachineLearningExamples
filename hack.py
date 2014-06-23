"""This generates stats from stock data"""
import cPickle as pickle
from helper import find_coordinates, normalize, avg

stocks = pickle.load(open("pickles/stocks.p","rb"))

def good_buy(date, stock,good_interest,bad_interest):
    """Return true if the stock is a good buy"""
    high = 1
    interest = 1.08
    dates = stock[0]
    stock = stock[1]
    try:
            later = dates [dates.index(date) + 52 * 5]
    except IndexError:
            later = dates[-1]
    good = (stock[later][high]) > (stock [date][high] * interest)
    change = (stock[later][high] - stock[date][high])/stock[date][high]
    if good:
        good_interest.append(change)
    else:
        bad_interest.append(change)
    return good

all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock))

for stock in all_points:
    normalize(stock)

# Produce map from years to buy/sell to list of data.
# Eg. years[2008][True][0][0] => Open of first good stock in 2008
good_interest = []
bad_interest = []
years = {}
for stock in all_points:
    for date in stock:
        raw_stock = stocks[all_points.index(stock)]
        good = good_buy(date, raw_stock,good_interest,bad_interest)

print avg(good_interest)
print avg(bad_interest)
print avg(good_interest + bad_interest)

pickle.dump(years,open("pickles/years.p","wb"))
pickle.dump(all_points,open("pickles/all_points.p","wb"))
