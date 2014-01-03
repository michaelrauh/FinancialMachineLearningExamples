import pickle
import math
pointMap = pickle.load(open("points.p","rb"))
dates = pickle.load(open("dates.p","rb"))


#make list of lows
lows = []
for date in dates:
    lows.append(pointMap[date][2])

yearLows = []
fiftytwoweeks= 5 * 52

#Find each 52 week low and add to yearLows. Map is not in order so iterate
#over dates

for i in range(fiftytwoweeks,len(dates)): #for dates after first buffer year
    if min(lows[i - fiftytwoweeks:i-1]) > lows[i]: # if lowest in last 52 weeks is greater than current
        yearLows.append(dates[i]) #then this is a 52 week low (save the date)


def numFiftyTwo(date):
    return 0

def slopeMin(minimum):
    return 0

def slopeMax(maximum):
    return 0

def findMax(date):
    return dates[0]

def findMin(maximum):
    return dates[0]

#Normalize the coordinates     
coordinates = {}
for date in yearLows:
    maximum = findMax(date)
    minimum = findMin(maximum)
    coordinates[date] = []
    coordinates[date].append(numFiftyTwo(date))
    coordinates[date].append(slopeMax(maximum))
    coordinates[date].append(slopeMin(minimum))
    coordinates[date].append(pointMap[date][2])
    coordinates[date].append(pointMap[date][1]-pointMap[date][2])
    coordinates[date].append(pointMap[date][4])
    coordinates[date].append(pointMap[maximum][4])
    coordinates[date].append(pointMap[minimum][4])
    coordinates[date].append(pointMap[maximum][1] - pointMap[maximum][2])
    coordinates[date].append(pointMap[minimum][1] - pointMap[minimum][2])

#For each 52 week low, we want to know:
#1: number of 52 week lows in last 10 days
#2: slope from local min
#3: slope from local max
#price,
#volatility,
#volume,
#volume on max,
#volume on min
#volatility on max, min

#These will be mapped to the date and pickled out
pickle.dump(coordinates,open("coordinates.p","wb"))
