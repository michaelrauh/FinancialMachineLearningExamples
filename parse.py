"""This script is converts from csv files to python structures"""
import os
import cPickle as pickle
from helper import parse

files = os.listdir(os.getcwd() + "\\data")  # All data file names
stocks = []
for name in files:
    file = open("data\\" + name, 'r')
    data = file.read()
    stocks.append(parse(data))

pickle.dump(stocks,open("pickles/stocks.p","wb"))
