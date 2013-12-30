import pickle
import math
pointMap = pickle.load(open("points.p","rb"))
dates = pickle.load(open("dates.p","rb"))


#make list of lows
lows = []
for date in dates:
    lows.append(pointMap[date][3])

yearLows = []
fiftytwoweeks= 5 * 52

#Find each 52 week low and add to yearLows. Map is not in order so iterate
#over dates

for i in range(fiftytwoweeks,len(dates)): #for dates after first buffer year
    if min(lows[i - fiftytwoweeks:i-1]) > lows[i]: # if lowest in last 52 weeks is greater than current
        yearLows.append(dates[i]) #then this is a 52 week low (save the date)


def numFiftyTwo(low):
    
    return 0

def slopeMin(minimum):
    return 0

def slopeMax(maximum):
    return 0

def findMin():
    return dates[0]

def findMax():
    return dates[0]
        
coordinates = {}
for low in yearLows:
    minimum = findMin()
    maximum = findMax()
    coordinates[low] = [numFiftyTwo(low),slopeMin(minimum),slopeMax(maximum),
                        pointMap[low][2],pointMap[low][1]-pointMap[low][2],pointMap[low][4],
                        pointMap[minimum][4],pointMap[maximum][4]]

#For each 52 week low, we want to know:
#1: number of 52 week lows in last 10 days
#2: slope from local min
#3: slope from local max
#price,
#volatility,
#volume,
#volume on max,
#volume on min

#These will be mapped to the date and pickled out
pickle.dump(coordinates,open("coordinates.p","wb"))
