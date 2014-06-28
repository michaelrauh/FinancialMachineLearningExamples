"""This generates stats from stock data"""zz
import cPickle as pickle
from helper import normalize, good_buy, find_max, slope_max, slope_min, find_min,avg, find_coordinates

stocks = pickle.load(open("pickles/stocks.p","rb"))

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in 4 week period before date"""
    count = 0
    last_month = dates[dates.index(date)-20:dates.index(date)]
    for day in last_month:
        count += yearLows.count(day)
    return count

def good_buy(date, stock,goods,bads):
    """Return true if the stock is a good buy"""
    opn = 0
    high = 1
    low = 2
    close = 3
    volume = 4
    lows = []
    dates = stock[0]
    point_map = stock[1]
    for date in dates:
        lows.append(point_map[date][low])
    yearLows = []
    fiftytwoweeks= 5 * 52

    for i in range(fiftytwoweeks, len(dates)):
        # For dates after first buffer year
        if min(lows[i - fiftytwoweeks:i - 1]) > lows[i]:
            # If lowest in last 52 weeks is greater than current
            yearLows.append(dates[i])

    for date in yearLows:
        year = 52 * 5
        month = 4*5
        day = 1
        
        interest = 1.08
        stock = point_map
        try:
                later = dates [dates.index(date) + month]
        except IndexError:
                later = dates[-1]
        good = (stock[later][high]) > (stock [date][high] * interest)
        if good:
            goods.append(num_fifty_two(date, yearLows, dates))
        else:
            bads.append(num_fifty_two(date, yearLows, dates))
    return good

all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock))

goods = []
bads = []
years = {}
i=0
for stock in all_points:
    for date in stock:
        if int(date[0:4]) in range(2000,2010): #years from 2000 to 2010
            raw_stock = stocks[all_points.index(stock)]
            good_buy(date, raw_stock, goods, bads)

goods.sort()
bads.sort()
from collections import Counter
print 'interest = 1.08, looking at 2000-2010, looking back one month and forward one month'
print 'good stocks:'
print 'min:',goods[0]
print '25%:',goods[(len(goods)/4)]
print '50%:',goods[(len(goods)/2)]
print '75%:',goods[(len(goods)/4) * 3]
print 'max:',goods[-1]
print'counts:'
data = Counter(goods)
print data.most_common()

print 'bad stocks:'
print 'min:',bads [0]
print '25%',bads[(len(bads)/4)]
print '50%',bads[(len(bads)/2)]
print '75%',bads[(len(bads)/4) * 3]
print 'max',bads[-1]
print 'counts:'
data = Counter(bads)
print data.most_common()
