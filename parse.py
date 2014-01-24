"""This script is concerned with taking in CSV files and making them into
usable python data structures"""
<<<<<<< HEAD

import os

files = os.listdir(os.getcwd() + "\\data")  # all data file names
=======

import os
<<<<<<< HEAD
import cPickle as pickle
from helper import *
    
files = os.listdir(os.getcwd()+ "\\data") #all data file names
=======

files = os.listdir(os.getcwd() + "\\data")  # all data file names
>>>>>>> ee872325f36602046db22bd0234eb7fc9f454a8d
>>>>>>> 986740360a67dda3edfdd47ee576c1ef004d748d
stocks = []
for name in files:
    file = open("data\\" + name, 'r')
    data = file.read()
<<<<<<< HEAD
=======
<<<<<<< HEAD
    stocks.append(parse(data))

pickle.dump(stocks,open("pickles/stocks.p","wb"))
=======
>>>>>>> 986740360a67dda3edfdd47ee576c1ef004d748d
    points = data.replace('\n', ',').split(',')  # split csv
    #create map from date to point data.
    point_map = {}
    dates = []
    for i in range(7, len(points) - 7, 7):
        point_map[points[i]] = (float(points[i + 1]), float(points[i + 2]),
                                float(points[i + 3]), float(points[i + 4]),
                                float(points[i + 5]), float(points[i + 6]))
        dates.append(points[i])
    dates.reverse()  # Dates earliest to latest
    stock = (dates, point_map)
    stocks.append(stock)
>>>>>>> ee872325f36602046db22bd0234eb7fc9f454a8d
