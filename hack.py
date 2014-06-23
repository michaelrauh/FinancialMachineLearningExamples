"""This generates stats from stock data"""
import cPickle as pickle
from helper import find_coordinates, normalize, avg

stocks = pickle.load(open("pickles/stocks.p","rb"))

def good_buy(date, stock,good_interest_soon,bad_interest_soon,good_interest_later,bad_interest_later,counters):
    """Return true if the stock is a good buy"""
    high = 1
    interest_soon = 1.0 #1.8/12
    interest_later = 1.0 #1.08
    dates = stock[0]
    stock = stock[1]
    try:
        much_later = dates [dates.index(date) + 52 * 5]
    except IndexError:
        much_later = dates[-1]
    try:
            later = dates [dates.index(date) + 4 * 5]
    except IndexError:
            later = dates[-1]
    good_soon = (stock[later][high]) > (stock [date][high] * interest_soon)
    good_later = (stock[much_later][high]) > (stock [date][high] * interest_later)
    change_soon = (stock[later][high] - stock[date][high])/stock[date][high]
    change_later = (stock[much_later][high] - stock[date][high])/stock[date][high]
    if good_soon and good_later:
        counters[0] +=1
        good_interest_soon.append(change_soon)
        good_interest_later.append(change_later)
    elif not good_soon and good_later:
        counters [1] +=1
        bad_interest_soon.append(change_soon)
        good_interest_soon.append(change_later)
    elif good_soon and not good_later:
        counters [2] += 1
        good_interest_soon.append(change_soon)
        bad_interest_later.append(change_later)
    else:
        counters [3] += 1
        bad_interest_soon.append(change_soon)
        bad_interest_later.append(change_later)

all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock))

for stock in all_points:
    normalize(stock)

# Produce map from years to buy/sell to list of data.
# Eg. years[2008][True][0][0] => Open of first good stock in 2008
good_interest_soon = []
bad_interest_soon = []
good_interest_later = []
bad_interest_later = []
counters = [0,0,0,0]
years = {}
for stock in all_points:
    for date in stock:
        raw_stock = stocks[all_points.index(stock)]
        good_buy(date, raw_stock,good_interest_soon,bad_interest_soon,good_interest_later,bad_interest_later,counters)

print 'this is for all stocks for all time. Good and bad are defined as gaining or losing value (interest = 1.0)'
print 'chance of good soon', len(good_interest_soon)/float(len(good_interest_soon + bad_interest_soon))
print 'average good soon', avg(good_interest_soon)
print 'average bad soon', avg(bad_interest_soon)
print 'average soon', avg(good_interest_soon + bad_interest_soon)
print 'chance of good later', len(good_interest_later)/float(len(good_interest_later + bad_interest_later))
print 'average good later', avg(good_interest_later)
print 'average bad later', avg(bad_interest_later)
print 'average later', avg(good_interest_later + bad_interest_later)
print 'good soon and later', counters[0]/float(sum(counters))
print 'bad soon and later', counters[3]/float(sum(counters))
print 'good soon bad later', counters[2]/float(sum(counters))
print 'bad soon good later', counters[1]/float(sum(counters))

print 'Of all good soon, how many go bad?', float(counters[2])/(counters[2]+counters[0])
print 'Of all the bad soon, how many go good?', float(counters[1])/(counters[1]+counters[3])


pickle.dump(years,open("pickles/years.p","wb"))
pickle.dump(all_points,open("pickles/all_points.p","wb"))
