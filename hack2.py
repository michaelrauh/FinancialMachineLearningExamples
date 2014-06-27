"""This generates stats from stock data"""
import cPickle as pickle
from helper import normalize, good_buy, find_max, slope_max, slope_min, find_min,avg

opn = 0
high = 1
low = 2
close = 3
volume = 4

stocks = pickle.load(open("pickles/stocks.p","rb"))

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in 10 day period before date"""
    count = 0
    last_ten = dates[dates.index(date)-10:dates.index(date)]
    for day in last_ten:
        count += yearLows.count(day)
    return count

def find_coordinates(stock, countLows):
    """Run technical analysis on a given stock"""
    # Make list of lows
    lows = []
    dates = stock[0]
    point_map = stock[1]
    for date in dates:
        lows.append(point_map[date][low])
    yearLows = []
    fiftytwoweeks= 5 * 52

    # Find each 52 week low and add to yearLows. Map is not in order so
    # iterate over dates
    for i in range(fiftytwoweeks, len(dates)):
        # For dates after first buffer year
        if min(lows[i - fiftytwoweeks:i - 1]) > lows[i]:
            # If lowest in last 52 weeks is greater than current
            yearLows.append(dates[i])
            # Then this is a 52 week low (save the date)

    coordinates = {}
    for date in yearLows:
        maximum = find_max(date,dates,point_map)
        minimum = find_min(maximum,dates,point_map)
        coordinates[date] = []
        # Number of 52 week lows in 10 day period #
        coordinates[date].append(num_fifty_two(date, yearLows, dates))
        countLows.append(num_fifty_two(date, yearLows, dates))

        # Slope from local max #
        coordinates[date].append(slope_max(dates, date, maximum, point_map))

        # Slope from local min #
        coordinates[date].append(slope_min(dates, date, minimum, point_map))

        # Volatility #
        coordinates[date].append(point_map[date][high] - point_map[date][low])

        # Volume #
        coordinates[date].append(point_map[date][volume])

        # Bull power #
        coordinates[date].append(point_map[maximum][volume])

        # Bear power #
        coordinates[date].append(point_map[minimum][volume])

        # Volatility at maximum #
        coordinates[date].append(point_map[maximum][high] - point_map[maximum][low])

        # Volatility at minimum #
        coordinates[date].append(point_map[minimum][high] - point_map[minimum][low])
    return coordinates

countLows = []
all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock, countLows))
print 'average number of 52 week lows in a two week period before the current 52 week low: ', avg(countLows)

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in a month long period before date"""
    count = 0
    last_month = dates[dates.index(date)-20:dates.index(date)]
    for day in last_month:
        count += yearLows.count(day)
    return count

countLows = []
all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock, countLows))
print 'average number of 52 week lows in a month long period before the current 52 week low: ', avg(countLows)

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in 6 week period before date"""
    count = 0
    last_month = dates[dates.index(date)-30:dates.index(date)]
    for day in last_month:
        count += yearLows.count(day)
    return count

countLows = []
all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock, countLows))
print 'average number of 52 week lows in a 6 week period before the current 52 week low: ', avg(countLows)

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in a two month period before date"""
    count = 0
    last_month = dates[dates.index(date)-40:dates.index(date)]
    for day in last_month:
        count += yearLows.count(day)
    return count

countLows = []
all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock, countLows))
print 'average number of 52 week lows in a two month period before the current 52 week low: ', avg(countLows)

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in a two month period before date"""
    count = 0
    last_month = dates[dates.index(date)-5:dates.index(date)]
    for day in last_month:
        count += yearLows.count(day)
    return count

countLows = []
all_points = []
for stock in stocks:
    all_points.append(find_coordinates(stock, countLows))
print 'average number of 52 week lows in a one week period before the current 52 week low: ', avg(countLows)
