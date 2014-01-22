"""This script is concerned with taking in CSV files and making them into usable python data structures"""
import os

files = os.listdir(os.getcwd()+ "\\data") #all data file names
stocks = []
for name in files:
    file = open("data\\" + name,'r')
    data = file.read()
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
    stocks.append(stock)

# Here we have a list of stocks. Each stock is a dates, point_map tuple
# dates is a list of dates
# point_map is a map from dates to a list of data

# Later, there will be a list of coordinates
# Then, this list will be split to a map. One entry for each year has each stock
