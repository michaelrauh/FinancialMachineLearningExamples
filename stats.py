"""This module is concerned with generating stats from stock data"""
#crypto slide 20

import math
from parse import *
import random

def num_fifty_two(date,yearLows,dates):
    #find number of 52 week lows in 10 day period before date
    count = 0
    last_ten = dates[dates.index(date)-10:dates.index(date)]
    for day in last_ten:
        count += yearLows.count(day)
    return count

def slope_min(date, minimum,point_map):
    #find slope from min to date
    rise = point_map[minimum][2] - point_map[date][2]
    run = dates.index(date) - dates.index(minimum)
    if (rise == 0):
        slope = 0
    else:
        slope = rise/run
    return slope

def slope_max(date, maximum,point_map):
    rise = point_map[maximum][1] - point_map[date][1]
    run = dates.index(date) - dates.index(maximum)
    if (rise == 0):
        slope = 0
    else:
        slope = rise/run
    return slope

def find_max(date):
    date_index = dates.index(date)
    while(point_map[dates[date_index]][1] < point_map[dates[date_index-1]][1]):
        date_index -= 1
    return dates[date_index]

def find_min(maximum):
    date_index = dates.index(maximum)
    while(point_map[dates[date_index]][2] > point_map[dates[date_index-1]][2]):
        date_index -= 1
    return dates[date_index]

def good_buy(date, info): #Returns True if stock is a good buy
    return random.choice([True,False])

all_points = []
for stock in stocks:
    #make list of lows
    lows = []
    dates = stock[0]
    point_map = stock[1]
    for date in dates:
        lows.append(point_map[date][2])
    yearLows = []
    fiftytwoweeks= 5 * 52

    #Find each 52 week low and add to yearLows. Map is not in order so iterate over dates
    for i in range(fiftytwoweeks,len(dates)): #for dates after first buffer year
        if min(lows[i - fiftytwoweeks:i-1]) > lows[i]: # if lowest in last 52 weeks is greater than current
            yearLows.append(dates[i]) #then this is a 52 week low (save the date)

    coordinates = {}
    for date in yearLows:
        maximum = find_max(date)
        minimum = find_min(maximum)
        coordinates[date] = []
        coordinates[date].append(num_fifty_two(date,yearLows,dates)) # Number of 52 week lows in 10 day period #
        coordinates[date].append(slope_max(date,maximum,point_map)) # Slope from local max # 
        coordinates[date].append(slope_min(date,minimum,point_map)) # Slope from local min #
        coordinates[date].append(point_map[date][1]-point_map[date][2]) # Volatility #
        coordinates[date].append(point_map[date][4]) # Volume #
        coordinates[date].append(point_map[maximum][4]) # Bull power #
        coordinates[date].append(point_map[minimum][4]) # Bear power #
        coordinates[date].append(point_map[maximum][1] - point_map[maximum][2]) # Volatility at maximum #
        coordinates[date].append(point_map[minimum][1] - point_map[minimum][2]) # Volatility at minimum #
    all_points.append(coordinates)

for stock in all_points:
    flipped = [[],[],[],[],[],[],[],[],[]]
    for date in stock:
        for i in range(0,len(flipped)):
            flipped[i].append(stock[date][i])
    for date in stock:
        for i in range(0,len(flipped)):
            stock[date][i] /= max(flipped[i]) #For now we will divide by max to get range from 0 to 1. Not ideal.

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
