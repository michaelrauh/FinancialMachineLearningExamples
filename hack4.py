"""Calculate average return by number of previous lows"""
import cPickle as pickle
from helper import normalize, good_buy, find_max, slope_max, slope_min, find_min,avg, find_coordinates

stocks = pickle.load(open("pickles/stocks.p","rb"))

def future_value(date, stock):
    """Return true if the stock is a good buy"""
    month = 20
    opn = 0
    interest = 1.08
    dates = stock[0]
    stock = stock[1]
    try:
            later = dates [dates.index(date) + month]
    except IndexError:
            later = dates[-1]
    value = ((stock[later][opn]) - stock[date][opn])/stock[later][opn]
    return value

stock = stocks[0]
all_points = find_coordinates(stock)
low_count = [[] for i in range(20)]
interest = .08

for date in all_points:
    low_count[all_points[date][0]].append(future_value(date,stock))

total = 0
for count in low_count:
    total += len(count)

print '|count|','likelihood |','mean |','0% |','25% |','50% |','75% |','100% |','percent dont lose |', 'percent reach goals |'
i =0
for count in low_count:
    try:
        likelihood = float(len(count))/total
        goods = 0
        makes = 0
        count.sort()
        average = avg(count)
        q0 = count[0]
        q1 = count[len(count)/4]
        q2 = count[len(count)/2]
        q3 = count [len(count)/4 * 3]
        q4 = count[-1]
        for item in count:
            if item > 0:
                makes += 1
        make = float(makes)/len(count)
        for item in count:
            if item > interest:
                goods += 1
        good = float(goods)/len(count)
        print round(i, 3),'   ',round(likelihood,3),'     ',round(average, 3),round(q0, 3),round(q1, 3),round(q2, 3),round(q3,3),round(q4,3),round(make,3),'               ',round(good,3)
        i+=1
    except:
        pass
        
