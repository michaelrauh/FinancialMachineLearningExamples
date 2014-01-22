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


def numFiftyTwo(date,yearLows,dates):
    #find number of 52 week lows in 10 day period before date
    count = 0
    last_ten = dates[dates.index(date)-10:dates.index(date)]
    for day in last_ten:
        count += yearLows.count(day)
    return count

def slopeMin(date, minimum,pointMap):
    #find slope from min to date
    rise = pointMap[date][2] - pointMap[minimum][2]
    run = dates.index(date) - dates.index(minimum)
    if (rise == 0):
        slope = 0
    else:
        slope = rise/run
    return slope

def slopeMax(date, maximum,pointMap):
    rise = pointMap[date][1] - pointMap[maximum][1]
    run = dates.index(date) - dates.index(maximum)
    if (rise == 0):
        slope = 0
    else:
        slope = rise/run
    return slope

def findMax(date):
    date_index = dates.index(date)
    while(pointMap[dates[date_index]][1] < pointMap[dates[date_index-1]][1]):
        date_index -= 1
    return dates[date_index]

def findMin(maximum):
    date_index = dates.index(maximum)
    while(pointMap[dates[date_index]][2] > pointMap[dates[date_index-1]][2]):
        date_index -= 1
    return dates[date_index]

#Normalize the coordinates- Seriously, don't forget to do this later   
coordinates = {}
for date in yearLows:
    maximum = findMax(date)
    minimum = findMin(maximum)
    coordinates[date] = []
    coordinates[date].append(numFiftyTwo(date,yearLows,dates))
    coordinates[date].append(slopeMax(date, maximum,pointMap))
    coordinates[date].append(slopeMin(date, minimum,pointMap))
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

#open,high,low,close,volume
