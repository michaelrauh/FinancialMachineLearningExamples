"""This file contains helper functions to improve readability of core code"""
from __future__ import division
import random
import math
import numpy as np
opn = 0
high = 1
low = 2
close = 3
volume = 4

def avg(points):
        """Find average of a list of points"""
        try:
                return sum(points)/len(points)
        except ZeroDivisionError:
                return 0
        except TypeError:
                return points
                
def distance(centroid, guess):
    """Compute the square of linear distance in n dimensions"""
    distance = 0
    for i in range (0,len(guess)):
        distance += (centroid[i]-guess[i])**2
    return distance

def extrapolate(avg, i, deg, back):
        """predict next value based upon history"""
        years = avg.keys()
        y = []
        for year in years[back:]:
                y.append(avg[year][i])
        x = range(len(y))
        z = np.polyfit(x,y,deg)
        p = np.poly1d(z)
        return p(len(y))
        #diff = avg[years[-1]][i] - avg[years[-2]][i]
        #return avg[years[-1]][i] + diff

def find_coordinates(stock):
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

def find_max(date,dates,point_map):
    """Find local max"""
    date_index = dates.index(date)
    while(point_map[dates[date_index]][high] < point_map[dates[date_index-1]][high]):
        date_index -= 1
    return dates[date_index]

def find_min(maximum,dates,point_map):
    """find local min"""
    date_index = dates.index(maximum)
    while(point_map[dates[date_index]][low] > point_map[dates[date_index-1]][low]):
        date_index -= 1
    return dates[date_index]

def good_buy(date, stock):
    """Return true if the stock is a good buy"""
    interest = 1.08
    dates = stock[0]
    stock = stock[1]
    try:
            later = dates [dates.index(date) + 52 * 5]
    except IndexError:
            later = dates[-1]
    good = (stock[later][high]) > (stock [date][high] * interest)
    return good

def normalize(stock):
    """Prevent different data scales from skewing data by returning a percentile"""
    flipped = [[] for i in range(9)]
    for date in stock:
        for i in range(9):
            flipped[i].append(stock[date][i])
    for i in range(len(flipped)):
        flipped[i] = list(set(flipped[i]))
    for i in range(len(flipped)):
        flipped[i].sort()
    for date in stock:
        for i in range(9):
            stock[date][i] = flipped[i].index(stock[date][i])/float(len(flipped[i]))

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in 10 day period before date"""
    count = 0
    last_ten = dates[dates.index(date)-10:dates.index(date)]
    for day in last_ten:
        count += yearLows.count(day)
    return count

def Parse (data):
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
    rise = point_map[maximum][high] - point_map[date][high]
    run = dates.index(date) - dates.index(maximum)
    try:
            return rise/run
    except ZeroDivisionError:
            return 0

def slope_min(dates,date, minimum,point_map):
    """Find slope from minimum to date"""
    rise = point_map[minimum][low] - point_map[date][low]
    run = dates.index(date) - dates.index(minimum)
    try:
            return rise/run
    except ZeroDivisionError:
            return 0
