import pickle
import math
pointMap = pickle.load(open("points.p","rb"))
dates = pickle.load(open("dates.p","rb"))

#make list of lows
lows = []
for date in dates:
    lows.append(pointMap[date][3])

low = 100000000
yearLows = []
fiftytwoweeks= 5 * 52

#Find each 52 week low and add to yearLows. Map is not in order so iterate
#over dates

for i in range(fiftytwoweeks,len(dates)): #for dates after first buffer year
    if min(lows[i - fiftytwoweeks:i-1]) > lows[i]: # if lowest in last 52 weeks is greater than current
        yearLows.append(dates[i]) #then this is a 52 week low (save the date)
        
        

#For each 52 week low, we want to know:
#1: number of 52 week lows in last 10 days
#2: slope from local min
#3: slope from local max

#These will be mapped to the date and pickled out
