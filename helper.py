"""This file contains helper functions to improve readability of core code"""
import random
import math

def avg(points):
        """Find average of a list of points"""
        if sum(points) != 0:
                return sum(points)/len(points)
        else:
                return 0

def distance(centroid, guess):
    """Compute the square of linear distance in n dimensions"""
    distance = 0
    for i in range (0,len(guess)):
        distance += (centroid[i]-guess[i])**2
    return distance

def extrapolate(avg, i):
        # Obviously not a very good function yet
        years = list(avg.keys())
        years.sort()
        diff = avg[years[-1]][i] - avg[years[-2]][i]
        return avg[years[-1]][i] + diff

def find_coordinates(stock):
    """Run technical analysis on a given stock"""
    # Make list of lows
    lows = []
    dates = stock[0]
    point_map = stock[1]
    for date in dates:
        lows.append(point_map[date][2])
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

        # Slope from local max #
        coordinates[date].append(slope_max(dates, date, maximum, point_map))

        # Slope from local min #
        coordinates[date].append(slope_min(dates, date, minimum, point_map))

        # Volatility #
        coordinates[date].append(point_map[date][1] - point_map[date][2])

        # Volume #
        coordinates[date].append(point_map[date][4])

        # Bull power #
        coordinates[date].append(point_map[maximum][4])

        # Bear power #
        coordinates[date].append(point_map[minimum][4])

        # Volatility at maximum #
        coordinates[date].append(point_map[maximum][1] - point_map[maximum][2])

        # Volatility at minimum #
        coordinates[date].append(point_map[minimum][1] - point_map[minimum][2])
    return coordinates

def find_max(date,dates,point_map):
    """Find local max"""
    date_index = dates.index(date)
    while(point_map[dates[date_index]][1] < point_map[dates[date_index-1]][1]):
        date_index -= 1
    return dates[date_index]

def find_min(maximum,dates,point_map):
    """find local min"""
    date_index = dates.index(maximum)
    while(point_map[dates[date_index]][2] > point_map[dates[date_index-1]][2]):
        date_index -= 1
    return dates[date_index]

def good_buy(date, info):
    """Return true if the stock is a good buy"""
    return random.choice([True,False])

def normalize(stock):
    """Prevent different data scales from skewing data"""
    flipped = [[],[],[],[],[],[],[],[],[]]
    for date in stock:
        for i in range(0,len(flipped)):
            flipped[i].append(stock[date][i])
    for date in stock:
        for i in range(0,len(flipped)):
            if stock[date][i] != 0:
                # For now we will divide by max to get range from 0 to 1.
                stock[date][i] /= max(flipped[i])
            else:
                stock[date][i] = 0

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in 10 day period before date"""
    count = 0
    last_ten = dates[dates.index(date)-10:dates.index(date)]
    for day in last_ten:
        count += yearLows.count(day)
    return count

def parse (data):
    """Create map from CSV"""
    points = data.replace('\n',',').split(',') # split csv
    #create map from date to point data.
    point_map = {}
    dates = []
    for i in range (7,len(points)-7,7):
        point_map[points[i]] = (float(points[i+1]),float(points[i+2]),
                                float(points[i+3]),float(points[i+4]),
                                float(points[i+5]),float(points[i+6]))
        dates.append(points[i])
    dates.reverse() #Dates earliest to latest
    stock = (dates,point_map)
    return stock

def slope_max(dates,date, maximum,point_map):
    """Find slope from maximum to date"""
    rise = point_map[maximum][1] - point_map[date][1]
    run = dates.index(date) - dates.index(maximum)
    if (rise == 0):
        slope = 0
    else:
        slope = rise/run
    return slope

def slope_min(dates,date, minimum,point_map):
    """Find slope from minimum to date"""
    rise = point_map[minimum][2] - point_map[date][2]
    run = dates.index(date) - dates.index(minimum)
    if (rise == 0):
        slope = 0
    else:
        slope = rise/run
    return slope
