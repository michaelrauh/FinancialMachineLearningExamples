import pickle

# This script is concerned with taking in CSV files and making them into usable
#python data structures and then pickling them out. For now, an example

file = open("table.csv",'r')
data = file.read()

points = data.replace('\n',',').split(',') # here is a list with each thing

#create map from date to point data. In practice, it may be useful to map open price or low to point data as we're focusing on 52 week lows
pointMap = {}
for i in range (0,len(points)-7,7):
    pointMap[points[i]] = (points[i+1],points[i+2],points[i+3],points[i+4],points[i+5],points[i+6])

#dump data for later usage

pickle.dump(pointMap,open("points.p","wb"))
