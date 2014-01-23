"""This script is concerned with taking in CSV files and making them into usable python data structures"""
import os
import cPickle as pickle
from helper import *
    
files = os.listdir(os.getcwd()+ "\\data") #all data file names
stocks = []
for name in files:
    file = open("data\\" + name,'r')
    data = file.read()
    stocks.append(parse(data))

pickle.dump(stocks,open("pickles/stocks.p","wb"))
